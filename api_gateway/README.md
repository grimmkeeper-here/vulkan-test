# API Gateway
### Gateway to communicate with users

##  Table of Contents
- [Tree](#tree)
- [Tech Stack](#tech-stack)

## Tree
```
API Gateway
├───cmd --> Init Main and router
├───config --> Load dot env to settings
├───handlers --> Adapter to map API and internal interfaces
├───internal
│   ├───entities --> Model
│   └───use_cases --> Use case call rpc to service
├───pb --> Generated proto files
├───pkg --> Utility services - gRPC client
└───protos --> Proto files
```

## Tech Stack
- Language: Golang
- API Framework: Gin
- RPC protocol framework: gRPC
