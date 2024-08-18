package use_cases

import (
	"context"

	"api_gateway/internal/entities"
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

func (uc *RoomUseCase) GetAvailableSeats(ctx context.Context, id int32) (*pb.GetAvailableSeatsResponse, error) {
	req := &pb.GetAvailableSeatsRequest{
		RoomId: id,
	}
	return uc.grpcClient.RoomServiceClient.GetAvailableSeats(ctx, req)
}

func (uc *RoomUseCase) ReserveSeats(ctx context.Context, id int32, seats []entities.Seat) (*pb.ReserveSeatsResponse, error) {
	req := &pb.ReserveSeatsRequest{
		RoomId: id,
		Seats:  make([]*pb.Seat, len(seats)),
	}
	for i, seat := range seats {
		req.Seats[i] = &pb.Seat{
			Id:   seat.ID,
			PosX: seat.PosX,
			PosY: seat.PosY,
		}
	}
	return uc.grpcClient.RoomServiceClient.ReserveSeats(ctx, req)
}

func (uc *RoomUseCase) CancelSeats(ctx context.Context, id int32, seatIds []int32) (*pb.CancelSeatsResponse, error) {
	req := &pb.CancelSeatsRequest{
		RoomId:  id,
		SeatIds: seatIds,
	}
	return uc.grpcClient.RoomServiceClient.CancelSeats(ctx, req)
}

func (uc *RoomUseCase) ListRoomSeats(ctx context.Context, id int32) (*pb.ListRoomSeatsResponse, error) {
	req := &pb.ListRoomSeatsRequest{
		RoomId: id,
	}
	return uc.grpcClient.RoomServiceClient.ListRoomSeats(ctx, req)
}
