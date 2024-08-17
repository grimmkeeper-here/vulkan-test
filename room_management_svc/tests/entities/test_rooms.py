"""
This file contains the tests for the rooms module.
"""

import pytest

from src.entities.rooms import Room
from src.entities.seats import Seat


def test_create_room():
    """
    Tests create room
    """
    # TEST CASE 1: create room with row negative
    with pytest.raises(ValueError) as _:
        Room(row=-1, col=1)

    # TEST CASE 2: create room with col negative
    with pytest.raises(ValueError) as _:
        Room(row=1, col=-1)

    # TEST CASE 3: create room with row is 0
    with pytest.raises(ValueError) as _:
        Room(row=0, col=1)

    # TEST CASE 4: create room with col is 0
    with pytest.raises(ValueError) as _:
        Room(row=1, col=0)

    # TEST CASE 5: happy case
    tmp_room = Room(row=1, col=1)
    assert tmp_room.row == 1
    assert tmp_room.col == 1


def test_room_add_seats():
    """
    Tests room add seats
    """
    tmp_room = Room(row=5, col=10)

    # TEST CASE 1: create seat with pos_x greater than row
    with pytest.raises(ValueError) as _:
        tmp_room.add_seats([Seat(pos_x=10, pos_y=1)])

    # TEST CASE 2: create seat with pos_y greater than col
    with pytest.raises(ValueError) as _:
        tmp_room.add_seats([Seat(pos_x=1, pos_y=10)])

    # TEST CASE 3: happy case
    tmp_room.add_seats([Seat(pos_x=1, pos_y=1)])
    assert len(tmp_room.seats) == 1

    # TEST CASE 4: add seat already in room
    with pytest.raises(ValueError) as _:
        tmp_room.add_seats([Seat(pos_x=1, pos_y=1)])

    # TEST CASE 5: add multiple seats
    tmp_room.add_seats([Seat(pos_x=2, pos_y=2), Seat(pos_x=3, pos_y=3)])
    assert len(tmp_room.seats) == 3

    # TEST CASE 6: add duplicate seats
    tmp_room.add_seats([Seat(pos_x=0, pos_y=1), Seat(pos_x=0, pos_y=1)])
    assert len(tmp_room.seats) == 4


def test_room_remove_seats():
    """
    Tests room remove seats
    """
    tmp_room = Room(row=5, col=10)

    # TEST CASE 1: remove seat with pos_x greater than row
    with pytest.raises(ValueError) as _:
        tmp_room.remove_seats([Seat(pos_x=10, pos_y=1)])

    # TEST CASE 2: remove seat with pos_y greater than col
    with pytest.raises(ValueError) as _:
        tmp_room.remove_seats([Seat(pos_x=1, pos_y=10)])

    # TEST CASE 3: remove seat not in room
    with pytest.raises(ValueError) as _:
        tmp_room.remove_seats([Seat(pos_x=1, pos_y=1)])

    # TEST CASE 4: happy case
    tmp_room.add_seats([Seat(pos_x=1, pos_y=1)])
    assert len(tmp_room.seats) == 1
    tmp_room.remove_seats([Seat(pos_x=1, pos_y=1)])
    assert len(tmp_room.seats) == 0

    # TEST CASE 5: remove multiple seats
    tmp_room.add_seats(
        [Seat(pos_x=1, pos_y=1), Seat(pos_x=2, pos_y=2), Seat(pos_x=3, pos_y=3)]
    )
    assert len(tmp_room.seats) == 3
    tmp_room.remove_seats([Seat(pos_x=1, pos_y=1), Seat(pos_x=2, pos_y=2)])
    assert len(tmp_room.seats) == 1

    # TEST CASE 6: remove duplicate seats
    tmp_room.add_seats([Seat(pos_x=1, pos_y=1)])
    assert len(tmp_room.seats) == 2
    tmp_room.remove_seats([Seat(pos_x=1, pos_y=1), Seat(pos_x=1, pos_y=1)])
    assert len(tmp_room.seats) == 1
