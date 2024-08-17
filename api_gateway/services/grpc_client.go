package services

import (
	"log"

	"api_gateway/pb"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type GRPCClient struct {
	RoomServiceClient pb.RoomServiceClient
}

func NewGRPCClient(addr string) (*GRPCClient, error) {
	conn, err := grpc.Dial(addr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Could not connect to gRPC server: %v", err)
		return nil, err
	}

	client := pb.NewRoomServiceClient(conn)
	return &GRPCClient{RoomServiceClient: client}, nil
}
