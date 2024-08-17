from concurrent import futures

import grpc
import pytest

from src.adapters.room_service import RoomService
from src.config import settings
from src.protos_generated import room_pb2_grpc


@pytest.fixture(scope="module")
def grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=settings.worker_count))
    room_pb2_grpc.add_RoomServiceServicer_to_server(RoomService(), server)
    server.add_insecure_port(f"{settings.grpc_host}:{settings.grpc_port}")
    server.start()
    yield server
    server.stop(None)
