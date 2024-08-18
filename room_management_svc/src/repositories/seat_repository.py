import json
from typing import List, Optional, Tuple

from src.config import settings
from src.entities.seats import Seat
from src.repositories.db_connection import get_db_connection
from src.services.redis_client import RedisClient


class SeatRepository:
    def __init__(self):
        self.redis_client = RedisClient()

    def list_seats_by_room_id(self, room_id: int) -> list[Seat]:
        # Check if the result is cached
        cached_room_seats = self.redis_client.get(f"room_seats_cache_{room_id}")
        if cached_room_seats:
            return [
                Seat.model_validate_json(item) for item in json.loads(cached_room_seats)
            ]

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, pos_x, pos_y FROM seat WHERE room_id = %s",
                (room_id,),
            )
            seats_data = cursor.fetchall()
            cursor.close()
            cached_room_seats = [
                Seat(
                    id=seat_data[0],
                    pos_x=seat_data[1],
                    pos_y=seat_data[2],
                )
                for seat_data in seats_data
            ]

            # Cache the result
            self.redis_client.set(
                f"room_seats_cache_{room_id}",
                json.dumps([item.model_dump_json() for item in cached_room_seats]),
                ex=settings.redis_key_ttl,
            )
            return cached_room_seats

    def reverse_seats(
        self, room_id: int, seats: list[Tuple[int, int]]
    ) -> list[Tuple[int, int]]:
        # Invalidate cache when a new room is added
        self.redis_client.client.delete(f"room_seats_cache_{room_id}")
        self.redis_client.delete_by_pattern(f"room_available_seats_{room_id}_*")

        with get_db_connection() as conn:
            cursor = conn.cursor()
            for pos_x, pos_y in seats:
                # Add seats to the room with insert record if not exists
                cursor.execute(
                    "INSERT INTO seat (room_id, pos_x, pos_y) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (room_id, pos_x, pos_y),
                )
            conn.commit()
            cursor.close()
            return seats

    def cancel_seats(self, room_id: int, seats: List[Seat]) -> None:
        # Invalidate cache when a new room is added
        self.redis_client.client.delete(f"room_seats_cache_{room_id}")
        self.redis_client.delete_by_pattern(f"room_available_seats_{room_id}_*")
        for seat in seats:
            self.redis_client.client.delete(f"seat_{seat.id}")

        with get_db_connection() as conn:
            cursor = conn.cursor()
            for seat in seats:
                # Lock row ---> Select for update
                cursor.execute(
                    "SELECT id FROM seat WHERE room_id = %s AND pos_x = %s AND pos_y = %s FOR UPDATE",
                    (room_id, seat.pos_x, seat.pos_y),
                )

                cursor.execute(
                    "DELETE FROM seat WHERE room_id = %s AND pos_x = %s AND pos_y = %s",
                    (room_id, seat.pos_x, seat.pos_y),
                )
            conn.commit()
            cursor.close()

    def get_seat_with_room_id(self, seat_id: int, room_id: int) -> Optional[Seat]:
        # Try to get room from cache
        cached_seat = self.redis_client.get(f"seat_{seat_id}")
        if cached_seat:
            return Seat.model_validate_json(json.loads(cached_seat))

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, pos_x, pos_y FROM seat WHERE id = %s AND room_id = %s",
                (seat_id, room_id),
            )
            seat_data = cursor.fetchone()
            cursor.close()
            if not seat_data:
                return None

            seat_db = Seat(
                id=seat_data[0],
                pos_x=seat_data[1],
                pos_y=seat_data[2],
            )

            # Cache the result
            self.redis_client.set(
                f"seat_{seat_id}",
                json.dumps(seat_db.model_dump_json()),
                ex=settings.redis_key_ttl,
            )

            return seat_db
