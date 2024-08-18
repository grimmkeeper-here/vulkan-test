package entities

type Seat struct {
	ID     int32  `json:"id"`
	RoomID int32  `json:"room_id"`
	PosX   *int32 `json:"pos_x"`
	PosY   *int32 `json:"pos_y"`
}

func NewSeat(id, roomID int32, posX, posY *int32) *Seat {
	return &Seat{
		ID:     id,
		RoomID: roomID,
		PosX:   posX,
		PosY:   posY,
	}
}
