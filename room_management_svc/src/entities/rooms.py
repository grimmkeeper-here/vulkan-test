from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from src.entities.seats import Seat


class Room(BaseModel):
    # Don't allow extra fields
    # Allow from attributes for orm
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: Optional[int] = None
    row: Annotated[int, Field(ge=1)]  # row must be greater than 0
    col: Annotated[int, Field(ge=1)]  # col must be greater than 0

    is_deleted: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    _seats: List[Seat] = []  # Use private variable to store seats

    # Getter for seats
    @property
    def seats(self) -> List[Seat]:
        # Return sorted available seats base on pos_x
        sorted_seats = self._seats.sort(key=lambda item: (item.pos_x, item.pos_y))
        return sorted_seats if sorted_seats else self._seats

    def validate_seat(self, seat: Seat):
        if seat.pos_x >= self.row:
            raise ValueError(f"Seat {seat} have pos_x is greater than row {self.row}")
        if seat.pos_y >= self.col:
            raise ValueError(f"Seat {seat} have pos_y is greater than col {self.col}")

    def add_seats(self, seats: List[Seat]):
        """
        Add seats to the room
        Args:
            seats: List of seats to add
        """
        # Validate seats
        for seat in seats:
            self.validate_seat(seat)

        # Check seats is already in the room
        for seat in seats:
            if seat in self._seats:
                raise ValueError(f"Seat {seat} is already in the room")

        # Add seats to the room and remove duplicates
        self._seats += list(set(seats) - set(self._seats))

    def remove_seats(self, seats: List[Seat]):
        """
        Remove seats from the room
        Args:
            seats: List of seats to remove
        """
        # Validate seats
        for seat in seats:
            self.validate_seat(seat)

        # Check if seats are in the room
        for seat in seats:
            if seat not in self._seats:
                raise ValueError(f"Seat {seat} is not in the room")

        # Remove seats from the room and remove duplicates
        self._seats = list(set(self._seats) - set(seats))
