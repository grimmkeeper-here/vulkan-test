import json
from typing import List, Optional, Tuple

from src.config import settings
from src.entities.rooms import Room
from src.entities.seats import Seat
from src.repositories.room_repository import RoomRepository
from src.repositories.seat_repository import SeatRepository
from src.services.redis_client import RedisClient


class RoomManagement:
    def __init__(self):
        self.room_repository = RoomRepository()
        self.seat_repository = SeatRepository()
        self.redis_client = RedisClient()

    def add_room(self, row: int, col: int) -> Optional[Room]:
        return self.room_repository.add_room(row=row, col=col)

    def remove_room(self, room_id: int):
        return self.room_repository.remove_room(room_id=room_id)

    def list_rooms(self) -> List[Room]:
        return self.room_repository.list_rooms()

    def get_room(self, room_id: int) -> Optional[Room]:
        return self.room_repository.get_room(room_id=room_id)

    def list_room_seats(self, room_id: int) -> List[Seat]:
        return self.seat_repository.list_seats_by_room_id(room_id=room_id)

    def get_room_available_seats(
        self, room: Room, min_distance: int
    ) -> List[Tuple[int, int]]:
        # Check if the result is cached
        cached_available_seats = self.redis_client.get(
            f"room_available_seats_{room.id}_{min_distance}"
        )
        if cached_available_seats:
            return json.loads(cached_available_seats)

        # Get all seats in the room
        list_room_seats = self.list_room_seats(room_id=room.id)
        room.add_seats(list_room_seats)

        available_seats = self.get_available_seats(room=room, min_distance=min_distance)

        # Cache the result
        self.redis_client.set(
            f"room_available_seats_{room.id}_{min_distance}",
            json.dumps(available_seats),
            ex=settings.redis_key_ttl,
        )
        return available_seats

    def reverse_room_seats(
        self, room: Room, seats: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        # DLM lock all seats
        # Aquire lock for all seats to prevent another flow from reserving the same seat
        lock_keys = []
        for seat in seats:
            tmp_lock = self.redis_client.acquire_lock(
                f"room_seat_{room.id}_{seat[0]}_{seat[1]}", settings.redis_key_ttl
            )
            if not tmp_lock:
                raise Exception(
                    f"Failed to acquire lock for room_seat_{room.id}_{seat[0]}_{seat[1]}"
                )
            lock_keys.append(tmp_lock)
        try:
            return self.seat_repository.reverse_seats(room_id=room.id, seats=seats)
        except Exception as e:
            raise e
        finally:
            # DLM unlock all seats
            for lock_key in lock_keys:
                self.redis_client.release_lock(lock_key)

    def cancel_room_seats(self, room: Room, seats: List[Seat]):
        # DLM lock all seats
        # Aquire lock for all seats to prevent another flow from cancel the same seat
        lock_keys = []
        for seat in seats:
            tmp_lock = self.redis_client.acquire_lock(
                f"room_seat_{room.id}_{seat.pos_x}_{seat.pos_y}", settings.redis_key_ttl
            )
            if not tmp_lock:
                raise Exception(
                    f"Failed to acquire lock for room_seat_{room.id}_{seat.pos_x}_{seat.pos_y}"
                )
            lock_keys.append(tmp_lock)
        try:
            return self.seat_repository.cancel_seats(room_id=room.id, seats=seats)
        except Exception as e:
            raise e
        finally:
            # DLM unlock all seats
            for lock_key in lock_keys:
                self.redis_client.release_lock(lock_key)

    def get_available_seats(
        self, room: Room, min_distance: int
    ) -> List[Tuple[int, int]]:
        # If all seats are available, return all seats
        if not room.seats:
            return [
                (pos_x, pos_y) for pos_x in range(room.row) for pos_y in range(room.col)
            ]
        # If all seats are taken, return empty list
        if len(room.seats) == room.row * room.col:
            return []

        available_seats: List[Tuple[int, int]] = []
        # If min_distance is 0, return all seats without taken seats
        if min_distance == 0:
            available_seats = list(
                set(
                    [
                        (pos_x, pos_y)
                        for pos_x in range(room.row)
                        for pos_y in range(room.col)
                    ]
                )
                - set([(seat.pos_x, seat.pos_y) for seat in room.seats])
            )

            # Return sorted available seats base on pos_x, pos_y
            available_seats = sorted(
                available_seats, key=lambda item: (item[0], item[1])
            )

            return available_seats

        # If some seats are taken, return available seats
        cur_position_seats: List[Tuple[int, int]] = [
            (seat.pos_x, seat.pos_y) for seat in room.seats
        ]

        for seat_pos_x, seat_pos_y in cur_position_seats:
            # Get all available_seats per already taken seat
            available_per_taken_seat: List[Tuple[int, int]] = (
                self.get_available_per_taken_seat(
                    room=room,
                    min_distance=min_distance,
                    seat_pos_x=seat_pos_x,
                    seat_pos_y=seat_pos_y,
                    cur_position_seats=cur_position_seats,
                )
            )

            # If available_seats is empty, assign available_per_taken_seat to available_seats
            if not available_seats:
                available_seats = available_per_taken_seat
                continue

            # Inner join available_seats and available_per_taken_seat
            available_seats = list(set(available_seats) & set(available_per_taken_seat))

        # Return sorted available seats base on pos_x, pos_y
        available_seats = sorted(available_seats, key=lambda item: (item[0], item[1]))

        return available_seats

    def get_available_per_taken_seat(
        self,
        room: Room,
        min_distance: int,
        seat_pos_x: int,
        seat_pos_y: int,
        cur_position_seats: List[Tuple[int, int]],
    ) -> List[Tuple[int, int]]:
        available_seats: List[Tuple[int, int]] = []

        for pos_x in range(room.row):
            # |pos_x - seat_x| + |pos_y - seat_y| = min_distance
            # Calculate abs_x
            abs_x: int = abs(seat_pos_x - pos_x)

            # If abs_x is greater than or equal to min_distance, all seats are available
            if abs_x >= min_distance:
                available_seats += list(
                    set([(pos_x, y) for y in range(room.col)]) - set(cur_position_seats)
                )
                continue

            # Calculate pos_y_min and pos_y_max
            abs_y: int = min_distance - abs_x
            pos_y_min: int = seat_pos_y - abs_y
            pos_y_max: int = seat_pos_y + abs_y

            # pos_y <= pos_y_min so if pos_y_min >= 0 and pos_y_min < self._room.col, pos_y = [0,pos_y_min+1]
            if pos_y_min >= 0 and pos_y_min < room.col:
                available_seats += list(
                    set([(pos_x, pos_y) for pos_y in range(0, pos_y_min + 1)])
                    - set(cur_position_seats)
                )

            # pos_y >= pos_y_max so if pos_y_max >= 0 and pos_y_max < self._room.col, pos_y = [pos_y_max, self._room.col]
            if pos_y_max >= 0 and pos_y_max < room.col:
                available_seats += list(
                    set([(pos_x, pos_y) for pos_y in range(pos_y_max, room.col)])
                    - set(cur_position_seats)
                )

        # Remove duplicate and remove existing seats
        available_seats = list(set(available_seats))
        return available_seats
