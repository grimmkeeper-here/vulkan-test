// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.5.1
// - protoc             v5.27.3
// source: protos/room.proto

package pb

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	emptypb "google.golang.org/protobuf/types/known/emptypb"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.64.0 or later.
const _ = grpc.SupportPackageIsVersion9

const (
	RoomService_AddRoom_FullMethodName    = "/room.RoomService/AddRoom"
	RoomService_RemoveRoom_FullMethodName = "/room.RoomService/RemoveRoom"
	RoomService_ListRooms_FullMethodName  = "/room.RoomService/ListRooms"
	RoomService_GetRoom_FullMethodName    = "/room.RoomService/GetRoom"
)

// RoomServiceClient is the client API for RoomService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type RoomServiceClient interface {
	AddRoom(ctx context.Context, in *AddRoomRequest, opts ...grpc.CallOption) (*AddRoomResponse, error)
	RemoveRoom(ctx context.Context, in *RemoveRoomRequest, opts ...grpc.CallOption) (*RemoveRoomResponse, error)
	ListRooms(ctx context.Context, in *emptypb.Empty, opts ...grpc.CallOption) (*ListRoomsResponse, error)
	GetRoom(ctx context.Context, in *GetRoomRequest, opts ...grpc.CallOption) (*GetRoomResponse, error)
}

type roomServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewRoomServiceClient(cc grpc.ClientConnInterface) RoomServiceClient {
	return &roomServiceClient{cc}
}

func (c *roomServiceClient) AddRoom(ctx context.Context, in *AddRoomRequest, opts ...grpc.CallOption) (*AddRoomResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(AddRoomResponse)
	err := c.cc.Invoke(ctx, RoomService_AddRoom_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *roomServiceClient) RemoveRoom(ctx context.Context, in *RemoveRoomRequest, opts ...grpc.CallOption) (*RemoveRoomResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(RemoveRoomResponse)
	err := c.cc.Invoke(ctx, RoomService_RemoveRoom_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *roomServiceClient) ListRooms(ctx context.Context, in *emptypb.Empty, opts ...grpc.CallOption) (*ListRoomsResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(ListRoomsResponse)
	err := c.cc.Invoke(ctx, RoomService_ListRooms_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *roomServiceClient) GetRoom(ctx context.Context, in *GetRoomRequest, opts ...grpc.CallOption) (*GetRoomResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(GetRoomResponse)
	err := c.cc.Invoke(ctx, RoomService_GetRoom_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// RoomServiceServer is the server API for RoomService service.
// All implementations must embed UnimplementedRoomServiceServer
// for forward compatibility.
type RoomServiceServer interface {
	AddRoom(context.Context, *AddRoomRequest) (*AddRoomResponse, error)
	RemoveRoom(context.Context, *RemoveRoomRequest) (*RemoveRoomResponse, error)
	ListRooms(context.Context, *emptypb.Empty) (*ListRoomsResponse, error)
	GetRoom(context.Context, *GetRoomRequest) (*GetRoomResponse, error)
	mustEmbedUnimplementedRoomServiceServer()
}

// UnimplementedRoomServiceServer must be embedded to have
// forward compatible implementations.
//
// NOTE: this should be embedded by value instead of pointer to avoid a nil
// pointer dereference when methods are called.
type UnimplementedRoomServiceServer struct{}

func (UnimplementedRoomServiceServer) AddRoom(context.Context, *AddRoomRequest) (*AddRoomResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method AddRoom not implemented")
}
func (UnimplementedRoomServiceServer) RemoveRoom(context.Context, *RemoveRoomRequest) (*RemoveRoomResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method RemoveRoom not implemented")
}
func (UnimplementedRoomServiceServer) ListRooms(context.Context, *emptypb.Empty) (*ListRoomsResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method ListRooms not implemented")
}
func (UnimplementedRoomServiceServer) GetRoom(context.Context, *GetRoomRequest) (*GetRoomResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetRoom not implemented")
}
func (UnimplementedRoomServiceServer) mustEmbedUnimplementedRoomServiceServer() {}
func (UnimplementedRoomServiceServer) testEmbeddedByValue()                     {}

// UnsafeRoomServiceServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to RoomServiceServer will
// result in compilation errors.
type UnsafeRoomServiceServer interface {
	mustEmbedUnimplementedRoomServiceServer()
}

func RegisterRoomServiceServer(s grpc.ServiceRegistrar, srv RoomServiceServer) {
	// If the following call pancis, it indicates UnimplementedRoomServiceServer was
	// embedded by pointer and is nil.  This will cause panics if an
	// unimplemented method is ever invoked, so we test this at initialization
	// time to prevent it from happening at runtime later due to I/O.
	if t, ok := srv.(interface{ testEmbeddedByValue() }); ok {
		t.testEmbeddedByValue()
	}
	s.RegisterService(&RoomService_ServiceDesc, srv)
}

func _RoomService_AddRoom_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(AddRoomRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(RoomServiceServer).AddRoom(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: RoomService_AddRoom_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(RoomServiceServer).AddRoom(ctx, req.(*AddRoomRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _RoomService_RemoveRoom_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(RemoveRoomRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(RoomServiceServer).RemoveRoom(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: RoomService_RemoveRoom_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(RoomServiceServer).RemoveRoom(ctx, req.(*RemoveRoomRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _RoomService_ListRooms_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(emptypb.Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(RoomServiceServer).ListRooms(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: RoomService_ListRooms_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(RoomServiceServer).ListRooms(ctx, req.(*emptypb.Empty))
	}
	return interceptor(ctx, in, info, handler)
}

func _RoomService_GetRoom_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GetRoomRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(RoomServiceServer).GetRoom(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: RoomService_GetRoom_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(RoomServiceServer).GetRoom(ctx, req.(*GetRoomRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// RoomService_ServiceDesc is the grpc.ServiceDesc for RoomService service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var RoomService_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "room.RoomService",
	HandlerType: (*RoomServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "AddRoom",
			Handler:    _RoomService_AddRoom_Handler,
		},
		{
			MethodName: "RemoveRoom",
			Handler:    _RoomService_RemoveRoom_Handler,
		},
		{
			MethodName: "ListRooms",
			Handler:    _RoomService_ListRooms_Handler,
		},
		{
			MethodName: "GetRoom",
			Handler:    _RoomService_GetRoom_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "protos/room.proto",
}
