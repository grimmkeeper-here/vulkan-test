from typing import Optional

from src.entities.seats import Seat
from src.repositories.seat_repository import SeatRepository


class SeatManagement:
    def __init__(self):
        self.seat_repository = SeatRepository()

    def get_seat_with_room_id(self, seat_id: int, room_id: int) -> Optional[Seat]:
        return self.seat_repository.get_seat_with_room_id(
            seat_id=seat_id, room_id=room_id
        )
