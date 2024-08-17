from src.protos_generated import room_pb2, room_pb2_grpc
from src.use_cases.room_management import RoomManagement


class RoomService(room_pb2_grpc.RoomServiceServicer):
    def __init__(self):
        self.room_management = RoomManagement()

    def AddRoom(self, request, context):
        room = self.room_management.add_room(request.row, request.col)
        if not room:
            return room_pb2.AddRoomResponse(status="Failed to add room")
        return room_pb2.AddRoomResponse(status="Room added", id=room.id)

    def RemoveRoom(self, request, context):
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
