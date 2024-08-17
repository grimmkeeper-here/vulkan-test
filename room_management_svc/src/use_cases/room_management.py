from typing import List, Optional, Tuple

from src.entities.rooms import Room
from src.repositories.room_repository import RoomRepository


class RoomManagement:
    def __init__(self):
        self.room_repository = RoomRepository()

    def add_room(self, row: int, col: int) -> Optional[Room]:
        return self.room_repository.add_room(row=row, col=col)

    def remove_room(self, room_id: int):
        return self.room_repository.remove_room(room_id=room_id)

    def list_rooms(self) -> List[Room]:
        return self.room_repository.list_rooms()

    def get_room(self, room_id: int) -> Optional[Room]:
        return self.room_repository.get_room(room_id=room_id)

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

        # If some seats are taken, return available seats
        available_seats: List[Tuple[int, int]] = []
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

        # Return sorted available seats base on pos_x
        available_seats = sorted(
            available_seats,
            key=lambda seat_position: (seat_position[0], seat_position[1]),
        )

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
