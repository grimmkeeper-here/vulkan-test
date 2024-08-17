import os
import sys
from concurrent import futures

import grpc
from loguru import logger

# Add the path to the parent directory
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from src.adapters.room_service import RoomService
from src.config import settings
from src.protos_generated import room_pb2_grpc


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=settings.worker_count))
    room_pb2_grpc.add_RoomServiceServicer_to_server(RoomService(), server)

    server.add_insecure_port(f"{settings.grpc_host}:{settings.grpc_port}")
    logger.info(f"Server started at port {settings.grpc_port}")

    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
