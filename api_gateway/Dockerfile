# Start with a Golang base image
FROM golang:1.23.0-alpine3.20 as builder

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN go build -o api_gateway ./cmd/main.go

FROM alpine:latest

COPY --from=builder /app/api_gateway /usr/bin/api_gateway

COPY .env .env

EXPOSE 8080

CMD ["api_gateway"]
