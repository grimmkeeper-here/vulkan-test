from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class Seat(BaseModel):
    # Don't allow extra fields
    # Allow from attributes for orm
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: Optional[int] = None
    pos_x: Annotated[int, Field(ge=0)]  # pos_x must be greater than 0
    pos_y: Annotated[int, Field(ge=0)]  # pos_y must be greater than 0

    is_deleted: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __eq__(self, other) -> bool:
        if isinstance(other, Seat):
            return self.pos_x == other.pos_x and self.pos_y == other.pos_y
        return False

    def __hash__(self) -> int:
        return hash((self.pos_x, self.pos_y))
