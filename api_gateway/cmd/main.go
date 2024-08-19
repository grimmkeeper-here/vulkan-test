package main

import (
	"log"

	"api_gateway/config"
	"api_gateway/handlers"
	"api_gateway/internal/use_cases"
	"api_gateway/pkg"

	"github.com/gin-gonic/gin"
)

func main() {
	// Load configuration
	cfg := config.LoadConfig()

	// Initialize gRPC client
	grpcClient, err := pkg.NewGRPCClient(cfg.GRPCServerAddress)
	if err != nil {
		log.Fatalf("Failed to connect to gRPC server: %v", err)
	}

	// Initialize use cases
	roomUseCase := use_cases.NewRoomUseCase(grpcClient)

	// Initialize Gin and set up routes
	r := gin.Default()
	roomHandler := handlers.NewRoomHandler(roomUseCase)

	r.POST("/rooms", roomHandler.AddRoom)
	r.DELETE("/rooms/:id", roomHandler.RemoveRoom)
	r.GET("/rooms/:id", roomHandler.GetRoom)
	r.GET("/rooms", roomHandler.ListRooms)
	r.GET("/rooms/:id/seats/available", roomHandler.GetAvailableSeats)
	r.POST("/rooms/:id/seats/reserve", roomHandler.ReserveSeats)
	r.DELETE("/rooms/:id/seats/cancel", roomHandler.CancelSeats)
	r.GET("/rooms/:id/seats", roomHandler.ListRoomSeats)
	r.GET("ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

	// Start the Gin server
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Failed to run Gin server: %v", err)
	}
}
