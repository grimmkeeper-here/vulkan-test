import json
from typing import Optional

from src.config import settings
from src.entities.rooms import Room
from src.repositories.db_connection import get_db_connection
from src.repositories.redis_client import RedisClient


class RoomRepository:
    def __init__(self):
        self.redis_client = RedisClient()

    def add_room(self, row: int, col: int) -> Optional[Room]:
        # Invalidate cache when a new room is added
        self.redis_client.client.delete("rooms_cache")

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO room (row, col) VALUES (%s, %s) RETURNING id, row, col, is_deleted, created_at, updated_at",
                (row, col),
            )
            room_data = cursor.fetchone()
            conn.commit()
            cursor.close()
            if room_data is None or cursor.description is None:
                return None
            return Room(
                id=room_data[0],
                row=room_data[1],
                col=room_data[2],
                is_deleted=room_data[3],
            )

    def remove_room(self, room_id: int):
        # Invalidate cache when a new room is added
        self.redis_client.client.delete("rooms_cache")

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE room SET is_deleted = TRUE WHERE id = %s", (room_id,)
            )
            conn.commit()
            cursor.close()

    def list_rooms(self) -> list[Room]:
        # Check if the result is cached
        cached_rooms = self.redis_client.get("rooms_cache")

        if cached_rooms:
            return [Room.model_validate_json(item) for item in json.loads(cached_rooms)]

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, row, col, is_deleted FROM room WHERE is_deleted = FALSE"
            )
            rooms_data = cursor.fetchall()
            cursor.close()

            # Cache the result
            cached_rooms = [
                Room(
                    id=room_data[0],
                    row=room_data[1],
                    col=room_data[2],
                    is_deleted=room_data[3],
                )
                for room_data in rooms_data
            ]

            self.redis_client.set(
                "rooms_cache",
                json.dumps([item.model_dump_json() for item in cached_rooms]),
                ex=settings.redis_key_ttl,
            )

            return cached_rooms

    def get_room(self, room_id: int) -> Optional[Room]:
        # Try to get room from cache
        cache_key = f"room_{room_id}"
        cached_room = self.redis_client.get(cache_key)
        if cached_room:
            return Room.model_validate_json(cached_room)

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, row, col, is_deleted FROM room WHERE id = %s AND is_deleted = FALSE",
                (room_id,),
            )
            room_data = cursor.fetchone()
            cursor.close()
            if room_data is None:
                return None
            cached_room = Room(
                id=room_data[0],
                row=room_data[1],
                col=room_data[2],
                is_deleted=room_data[3],
            )

            self.redis_client.set(
                cache_key, cached_room.model_dump_json(), ex=settings.redis_key_ttl
            )

            return cached_room
