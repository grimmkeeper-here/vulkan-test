package handlers

import (
	"net/http"
	"strconv"

	"api_gateway/internal/use_cases"

	"github.com/gin-gonic/gin"
)

type RoomHandler struct {
	roomUseCase *use_cases.RoomUseCase
}

func NewRoomHandler(roomUseCase *use_cases.RoomUseCase) *RoomHandler {
	return &RoomHandler{roomUseCase: roomUseCase}
}

func (h *RoomHandler) AddRoom(c *gin.Context) {
	var req struct {
		Row int32 `json:"row"`
		Col int32 `json:"col"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	res, err := h.roomUseCase.AddRoom(c, req.Row, req.Col)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, res)
}

func (h *RoomHandler) RemoveRoom(c *gin.Context) {
	roomID, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid room ID"})
		return
	}

	res, err := h.roomUseCase.RemoveRoom(c, int32(roomID))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, res)
}

func (h *RoomHandler) GetRoom(c *gin.Context) {
    roomID, err := strconv.Atoi(c.Param("id"))
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid room ID"})
        return
    }

    res, err := h.roomUseCase.GetRoom(c, int32(roomID))
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusOK, res)
}

func (h *RoomHandler) ListRooms(c *gin.Context) {
    res, err := h.roomUseCase.ListRooms(c)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusOK, res)
}
