# Start with a Golang base image
FROM golang:1.23.0-alpine3.20 as builder

# Set the working directory
WORKDIR /app

# Copy the go mod and sum files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the source code
COPY . .

# Build the Go app
RUN go build -o api_gateway ./cmd/main.go

# Start a new stage from scratch
FROM alpine:latest

# Copy the built binary from the previous stage
COPY --from=builder /app/api_gateway /usr/bin/api_gateway

# Copy .env file
COPY .env .env

# Expose port 8080
EXPOSE 8080

# Run the binary
CMD ["api_gateway"]
