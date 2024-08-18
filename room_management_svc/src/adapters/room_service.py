from typing import List, Tuple

from src.config import settings
from src.entities.seats import Seat
from src.protos_generated import room_pb2, room_pb2_grpc
from src.use_cases.room_management import RoomManagement
from src.use_cases.seat_management import SeatManagement


class RoomService(room_pb2_grpc.RoomServiceServicer):
    def __init__(self):
        self.room_management = RoomManagement()
        self.seat_management = SeatManagement()

    def AddRoom(self, request, context):
        room = self.room_management.add_room(request.row, request.col)
        if not room:
            return room_pb2.AddRoomResponse(status="Failed to add room")
        return room_pb2.AddRoomResponse(status="Room added", id=room.id)

    def RemoveRoom(self, request, context):
        # Check if the room exists
        room = self.room_management.get_room(request.id)
        if not room:
            return room_pb2.RemoveRoomResponse(status="Room not found")

        self.room_management.remove_room(request.id)
        return room_pb2.RemoveRoomResponse(status="Room removed")

    def ListRooms(self, request, context):
        rooms = self.room_management.list_rooms()
        return room_pb2.ListRoomsResponse(
            rooms=[
                room_pb2.Room(
                    id=room.id,
                    row=room.row,
                    col=room.col,
                )
                for room in rooms
            ]
        )

    def GetRoom(self, request, context):
        room = self.room_management.get_room(request.id)
        if not room:
            return room_pb2.GetRoomResponse(status="Room not found")
        return room_pb2.GetRoomResponse(
            room=room_pb2.Room(
                id=room.id,
                row=room.row,
                col=room.col,
            )
        )

    def ListRoomSeats(self, request, context):
        # Check if the room exists
        room = self.room_management.get_room(request.room_id)
        if not room:
            return room_pb2.ListRoomSeatsResponse(status="Room not found")

        seats = self.room_management.list_room_seats(request.room_id)
        return room_pb2.ListRoomSeatsResponse(
            seats=[
                room_pb2.Seat(
                    id=seat.id,
                    pos_x=seat.pos_x,
                    pos_y=seat.pos_y,
                )
                for seat in seats
            ]
        )

    def GetAvailableSeats(self, request, context):
        # Check if the room exists
        room = self.room_management.get_room(request.room_id)
        if not room:
            return room_pb2.GetAvailableSeatsResponse(status="Room not found")

        available_seats = self.room_management.get_room_available_seats(
            room=room, min_distance=settings.min_distance
        )
        return room_pb2.GetAvailableSeatsResponse(
            seats=[
                room_pb2.Seat(
                    pos_x=seat[0],
                    pos_y=seat[1],
                )
                for seat in available_seats
            ]
        )

    def ReserveSeats(self, request, context):
        # Check if the room exists
        room = self.room_management.get_room(request.room_id)
        if not room:
            return room_pb2.ReserveSeatsResponse(status="Room not found")

        # Check if seats are in the room
        for seat in request.seats:
            if seat.pos_x >= room.row:
                return room_pb2.ReserveSeatsResponse(
                    status=f"Seat {seat} have pos_x is greater than row {room.row}"
                )
            if seat.pos_y >= room.col:
                return room_pb2.ReserveSeatsResponse(
                    status=f"Seat {seat} have pos_y is greater than col {room.col}"
                )

        # Check if seats are already in the room
        for seat in request.seats:
            # Check pos_x and pos_y are the same
            for room_seat in self.room_management.list_room_seats(room.id):
                if seat.pos_x == room_seat.pos_x and seat.pos_y == room_seat.pos_y:
                    return room_pb2.ReserveSeatsResponse(
                        status=f"Seat x:{seat.pos_x} - y:{seat.pos_y} is already in the room"
                    )

        # Check if seats in available_seats
        available_seats: List[Tuple[int, int]] = (
            self.room_management.get_room_available_seats(
                room=room, min_distance=settings.min_distance
            )
        )
        for seat in request.seats:
            is_available = False
            for available_seat in available_seats:
                if seat.pos_x == available_seat[0] and seat.pos_y == available_seat[1]:
                    is_available = True
                    break
        if not is_available:
            return room_pb2.ReserveSeatsResponse(
                status=f"Seat x:{seat.pos_x} - y:{seat.pos_y} is not available"
            )

        seats = self.room_management.reverse_room_seats(
            room=room, seats=[(seat.pos_x, seat.pos_y) for seat in request.seats]
        )
        return room_pb2.ReserveSeatsResponse(
            seats=[
                room_pb2.Seat(
                    pos_x=seat[0],
                    pos_y=seat[1],
                )
                for seat in seats
            ]
        )

    def CancelSeats(self, request, context):
        # Check if the room exists
        room = self.room_management.get_room(request.room_id)
        if not room:
            return room_pb2.CancelSeatsResponse(status="Room not found")

        if not request.seat_ids:
            return room_pb2.CancelSeatsResponse(status="Seat ids is empty")

        list_seats: List[Seat] = []
        # Check seats in db
        for seat_id in request.seat_ids:
            seat = self.seat_management.get_seat_with_room_id(
                seat_id, room_id=request.room_id
            )
            if not seat:
                return room_pb2.CancelSeatsResponse(
                    status=f"Seat id {seat_id} is not found"
                )

            # Check if seats are valid with the room
            if seat.pos_x >= room.row:
                return room_pb2.CancelSeatsResponse(
                    status=f"Seat {seat} have pos_x is greater than row {room.row}"
                )
            if seat.pos_y >= room.col:
                return room_pb2.CancelSeatsResponse(
                    status=f"Seat {seat} have pos_y is greater than col {room.col}"
                )
            list_seats.append(seat)

        self.room_management.cancel_room_seats(room=room, seats=list_seats)
        return room_pb2.CancelSeatsResponse(status="Seats are canceled")
