package use_cases

import (
	"context"

	"api_gateway/pb"
	"api_gateway/services"
	"google.golang.org/protobuf/types/known/emptypb"
)

type RoomUseCase struct {
	grpcClient *services.GRPCClient
}

func NewRoomUseCase(grpcClient *services.GRPCClient) *RoomUseCase {
	return &RoomUseCase{grpcClient: grpcClient}
}

func (uc *RoomUseCase) AddRoom(ctx context.Context, row int32, col int32) (*pb.AddRoomResponse, error) {
	req := &pb.AddRoomRequest{
		Row: row,
		Col: col,
	}
	return uc.grpcClient.RoomServiceClient.AddRoom(ctx, req)
}

func (uc *RoomUseCase) RemoveRoom(ctx context.Context, id int32) (*pb.RemoveRoomResponse, error) {
	req := &pb.RemoveRoomRequest{
		Id: id,
	}
	return uc.grpcClient.RoomServiceClient.RemoveRoom(ctx, req)
}

func (uc *RoomUseCase) GetRoom(ctx context.Context, id int32) (*pb.GetRoomResponse, error) {
	req := &pb.GetRoomRequest{
		Id: id,
	}
	return uc.grpcClient.RoomServiceClient.GetRoom(ctx, req)
}

func (uc *RoomUseCase) ListRooms(ctx context.Context) (*pb.ListRoomsResponse, error) {
	emptyRequest := &emptypb.Empty{}
	return uc.grpcClient.RoomServiceClient.ListRooms(ctx, emptyRequest)
}
