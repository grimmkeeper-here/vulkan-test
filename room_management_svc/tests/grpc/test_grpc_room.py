import grpc
from google.protobuf import empty_pb2

from src.config import settings
from src.protos_generated import room_pb2, room_pb2_grpc


def test_add_room(grpc_server):
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
        assert response.id is not None


def test_remove_room(grpc_server):
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
        response = stub.RemoveRoom(room_pb2.RemoveRoomRequest(id=response.id))


def test_list_rooms(grpc_server):
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        _ = stub.ListRooms(empty_pb2.Empty())


def test_get_room(grpc_server):
    # TEST CASE 1: happy case
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
        response = stub.GetRoom(room_pb2.GetRoomRequest(id=response.id))
        assert response.room.row == 10
        assert response.room.col == 20
        assert response.room.id is not None

    # TEST CASE 2: room not found
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.GetRoom(room_pb2.GetRoomRequest(id=999))


def test_list_room_seats(grpc_server):
    # TEST CASE 1: happy case
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
        response = stub.ListRoomSeats(
            room_pb2.ListRoomSeatsRequest(room_id=response.id)
        )
        assert len(response.seats) == 0

    # TEST CASE 2: room not found
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.ListRoomSeats(room_pb2.ListRoomSeatsRequest(room_id=999))
        assert response.status == "Room not found"


def test_get_room_available_seats(grpc_server):
    # TEST CASE 1: happy case
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
        response = stub.GetAvailableSeats(
            room_pb2.GetAvailableSeatsRequest(room_id=response.id)
        )
        assert len(response.seats) == 200

    # TEST CASE 2: room not found
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.GetAvailableSeats(
            room_pb2.GetAvailableSeatsRequest(room_id=999)
        )
        assert response.status == "Room not found"


def test_reverse_room_seats(grpc_server):
    # TEST CASE 1: happy case
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
        response = stub.ReserveSeats(
            room_pb2.ReserveSeatsRequest(
                room_id=response.id, seats=[room_pb2.Seat(pos_x=0, pos_y=0)]
            )
        )
        assert len(response.seats) == 1

    # TEST CASE 2: room not found
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.ReserveSeats(
            room_pb2.ReserveSeatsRequest(
                room_id=999, seats=[room_pb2.Seat(pos_x=0, pos_y=0)]
            )
        )
        assert response.status == "Room not found"

    # TEST CASE 3: seat pos_x is greater than row
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
        response = stub.ReserveSeats(
            room_pb2.ReserveSeatsRequest(
                room_id=response.id, seats=[room_pb2.Seat(pos_x=10, pos_y=0)]
            )
        )
        assert "greater than row" in response.status

    # TEST CASE 4: seat pos_y is greater than col
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
        response = stub.ReserveSeats(
            room_pb2.ReserveSeatsRequest(
                room_id=response.id, seats=[room_pb2.Seat(pos_x=0, pos_y=20)]
            )
        )
        assert "greater than col" in response.status

    # TEST CASE 5: seat is already in the room
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
        room_id = response.id
        response = stub.ReserveSeats(
            room_pb2.ReserveSeatsRequest(
                room_id=room_id, seats=[room_pb2.Seat(pos_x=0, pos_y=0)]
            )
        )
        response = stub.ReserveSeats(
            room_pb2.ReserveSeatsRequest(
                room_id=room_id, seats=[room_pb2.Seat(pos_x=0, pos_y=0)]
            )
        )
        # assert "is already in the room" in response.status

    # TEST CASE 6: all seats are available
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=5, col=10))
        response = stub.GetAvailableSeats(
            room_pb2.GetAvailableSeatsRequest(room_id=response.id)
        )
        assert len(response.seats) == 50

    # TEST CASE 7: all seats are taken
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=5, col=10))
        room_id = response.id
        response = stub.ReserveSeats(
            room_pb2.ReserveSeatsRequest(
                room_id=room_id,
                seats=[
                    room_pb2.Seat(pos_x=x, pos_y=y) for x in range(5) for y in range(10)
                ],
            )
        )
        response = stub.GetAvailableSeats(
            room_pb2.GetAvailableSeatsRequest(room_id=room_id)
        )
        assert len(response.seats) == 0

    # TEST CASE 8: seat is not in available seats
    with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
        stub = room_pb2_grpc.RoomServiceStub(channel)
        response = stub.AddRoom(room_pb2.AddRoomRequest(row=5, col=10))
        room_id = response.id
        response = stub.ReserveSeats(
            room_pb2.ReserveSeatsRequest(
                room_id=room_id, seats=[room_pb2.Seat(pos_x=0, pos_y=0)]
            )
        )
        response = stub.GetAvailableSeats(
            room_pb2.GetAvailableSeatsRequest(room_id=room_id)
        )
        response = stub.ReserveSeats(
            room_pb2.ReserveSeatsRequest(
                room_id=room_id, seats=[room_pb2.Seat(pos_x=0, pos_y=1)]
            )
        )
        assert "not available" in response.status

    def test_cancel_seats(grpc_server):
        # TEST CASE 1: happy case
        with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
            stub = room_pb2_grpc.RoomServiceStub(channel)
            response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
            room_id = response.id
            response = stub.ReserveSeats(
                room_pb2.ReserveSeatsRequest(
                    room_id=room_id, seats=[room_pb2.Seat(pos_x=0, pos_y=0)]
                )
            )
            response = stub.CancelSeats(
                room_pb2.CancelSeatsRequest(
                    room_id=room_id, seat_ids=[room_pb2.Seat(pos_x=0, pos_y=0)]
                )
            )
            assert len(response.seats) == 0

        # TEST CASE 2: room not found
        with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
            stub = room_pb2_grpc.RoomServiceStub(channel)
            response = stub.CancelSeats(
                room_pb2.CancelSeatsRequest(
                    room_id=999, seat_ids=[room_pb2.Seat(pos_x=0, pos_y=0)]
                )
            )
            assert response.status == "Room not found"

        # TEST CASE 3: seat pos_x is greater than row
        with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
            stub = room_pb2_grpc.RoomServiceStub(channel)
            response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
            response = stub.CancelSeats(
                room_pb2.CancelSeatsRequest(
                    room_id=response.id, seat_ids=[room_pb2.Seat(pos_x=10, pos_y=0)]
                )
            )
            assert "greater than row" in response.status

        # TEST CASE 4: seat pos_y is greater than col
        with grpc.insecure_channel(f"localhost:{settings.grpc_port}") as channel:
            stub = room_pb2_grpc.RoomServiceStub(channel)
            response = stub.AddRoom(room_pb2.AddRoomRequest(row=10, col=20))
            response = stub.CancelSeats(
                room_pb2.CancelSeatsRequest(
                    room_id=response.id, seat_ids=[room_pb2.Seat(pos_x=0, pos_y=20)]
                )
            )
            assert "greater than col" in response.status
