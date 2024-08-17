"""
This module contains tests for the seats module.
"""

import pytest

from src.entities.seats import Seat


def test_create_seat():
    """
    Tests create seat
    """
    # TEST CASE 1: create seat with pos_x negative
    with pytest.raises(ValueError) as _:
        Seat(pos_x=-1, pos_y=1)

    # TEST CASE 2: create seat with pos_y negative
    with pytest.raises(ValueError) as _:
        Seat(pos_x=1, pos_y=-1)

    # TEST CASE 3: create seat with pos_x is 0
    tmp_seat = Seat(pos_x=0, pos_y=1)
    print(Seat(pos_x=0, pos_y=1))
    assert tmp_seat.pos_x == 0
    assert tmp_seat.pos_y == 1

    # TEST CASE 4: create seat with pos_y is 0
    tmp_seat = Seat(pos_x=1, pos_y=0)
    assert tmp_seat.pos_x == 1
    assert tmp_seat.pos_y == 0
