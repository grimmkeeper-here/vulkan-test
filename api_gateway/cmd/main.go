package main

import (
	"log"

	"api_gateway/config"
	"api_gateway/handlers"
	"api_gateway/internal/use_cases"
	"api_gateway/services"

	"github.com/gin-gonic/gin"
)

func main() {
	// Load configuration
	cfg := config.LoadConfig()

	// Initialize gRPC client
	grpcClient, err := services.NewGRPCClient(cfg.GRPCServerAddress)
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

	// Start the Gin server
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Failed to run Gin server: %v", err)
	}
}
