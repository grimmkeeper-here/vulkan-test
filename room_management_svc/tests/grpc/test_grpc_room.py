import grpc
from google.protobuf import empty_pb2

from src.config import settings
from src.protos_generated import room_pb2, room_pb2_grpc


def test_add_room(grpc_server):
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
        assert response.status == "Room added"
        assert response.id is not None


def test_remove_room(grpc_server):
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
        response = stub.RemoveRoom(room_pb2.RemoveRoomRequest(id=response.id))
        assert response.status == "Room removed"


def test_list_rooms(grpc_server):
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        _ = stub.ListRooms(empty_pb2.Empty())


def test_get_room(grpc_server):
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
        response = stub.GetRoom(room_pb2.GetRoomRequest(id=response.id))
        assert response.room.row == 10
        assert response.room.col == 20
        assert response.room.id is not None
