"""
This module contains tests for the room management module.
"""

from typing import Counter, List, Tuple

from src.entities.rooms import Room
from src.entities.seats import Seat
from src.use_cases.room_management import RoomManagement


def test_get_available_seats():
    """
    Tests get available seats
    """
    room = Room(row=5, col=10)

    # TEST CASE 1: all seats are available
    room_management = RoomManagement()
    available_seats = room_management.get_available_seats(room=room, min_distance=5)
    assert len(available_seats) == 50

    # TEST CASE 2: some seats are taken
    room.add_seats([Seat(pos_x=0, pos_y=1)])
    available_seats = room_management.get_available_seats(room=room, min_distance=5)
    expected: List[Tuple[int, int]] = [
        (0, 6),
        (0, 7),
        (0, 8),
        (0, 9),
        (1, 5),
        (1, 6),
        (1, 7),
        (1, 8),
        (1, 9),
        (2, 4),
        (2, 5),
        (2, 6),
        (2, 7),
        (2, 8),
        (2, 9),
        (3, 3),
        (3, 4),
        (3, 5),
        (3, 6),
        (3, 7),
        (3, 8),
        (3, 9),
        (4, 0),
        (4, 2),
        (4, 3),
        (4, 4),
        (4, 5),
        (4, 6),
        (4, 7),
        (4, 8),
        (4, 9),
    ]

    assert len(available_seats) == len(expected)
    assert Counter(available_seats) == Counter(expected)

    # TEST CASE 3: More seats
    room.add_seats([Seat(pos_x=0, pos_y=2), Seat(pos_x=0, pos_y=3)])
    available_seats = room_management.get_available_seats(room=room, min_distance=5)
    expected = [
        (0, 8),
        (0, 9),
        (1, 7),
        (1, 8),
        (1, 9),
        (2, 6),
        (2, 7),
        (2, 8),
        (2, 9),
        (3, 5),
        (3, 6),
        (3, 7),
        (3, 8),
        (3, 9),
        (4, 0),
        (4, 4),
        (4, 5),
        (4, 6),
        (4, 7),
        (4, 8),
        (4, 9),
    ]

    assert len(available_seats) == len(expected)
    assert Counter(available_seats) == Counter(expected)

    # TEST CASE 4: More seats
    room.add_seats([Seat(pos_x=4, pos_y=8), Seat(pos_x=4, pos_y=9)])
    available_seats = room_management.get_available_seats(room=room, min_distance=5)
    expected = [(4, 0)]
    assert len(available_seats) == 1
    assert Counter(available_seats) == Counter(expected)

    # TEST CASE 5: All seats are taken
    room = Room(row=5, col=10)
    room.add_seats([Seat(pos_x=x, pos_y=y) for x in range(5) for y in range(10)])
    available_seats = room_management.get_available_seats(room=room, min_distance=5)
    assert len(available_seats) == 0

    # TEST CASE 6: min_distance is 0
    room = Room(row=5, col=10)
    room.add_seats([Seat(pos_x=0, pos_y=1)])
    available_seats = room_management.get_available_seats(room=room, min_distance=0)
    expected = [
        (0, 0),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (0, 7),
        (0, 8),
        (0, 9),
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (1, 7),
        (1, 8),
        (1, 9),
        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (2, 7),
        (2, 8),
        (2, 9),
        (3, 0),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 4),
        (3, 5),
        (3, 6),
        (3, 7),
        (3, 8),
        (3, 9),
        (4, 0),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 4),
        (4, 5),
        (4, 6),
        (4, 7),
        (4, 8),
        (4, 9),
    ]
    print(available_seats)
    assert len(available_seats) == len(expected)
