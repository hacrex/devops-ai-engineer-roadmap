#!/bin/bash
# Day 1: Linux Containers - Example Scripts
# Demonstrates basic container operations

set -e

echo "=========================================="
echo "LINUX CONTAINERS - EXAMPLE SCRIPTS"
echo "=========================================="

# =============================================================================
# Example 1: Basic Docker Commands
# =============================================================================
example_basic_docker() {
    echo ""
    echo "1. BASIC DOCKER COMMANDS"
    echo "------------------------------------------"
    
    cat << 'EOF'
# Pull an image
docker pull alpine:latest

# Run a container interactively
docker run -it alpine sh

# Run a container with volume mount
docker run -v $(pwd):/app -w /app alpine ls -la

# Run a container with port mapping
docker run -p 8080:80 nginx:alpine

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List images
docker images

# Remove a container
docker rm <container_id>

# Remove an image
docker rmi <image_id>
EOF
}

# =============================================================================
# Example 2: Building Custom Images
# =============================================================================
example_build_image() {
    echo ""
    echo "2. BUILDING CUSTOM IMAGES"
    echo "------------------------------------------"
    
    # Create a sample Dockerfile
    cat > Dockerfile.example << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
EOF
    
    echo "Created Dockerfile.example"
    echo ""
    echo "Build commands:"
    echo "  docker build -t my-python-app ."
    echo "  docker build --no-cache -t my-python-app:latest ."
    echo ""
    echo "Run the built image:"
    echo "  docker run -p 8000:8000 my-python-app"
}

# =============================================================================
# Example 3: Docker Compose Multi-Container Setup
# =============================================================================
example_docker_compose() {
    echo ""
    echo "3. DOCKER COMPOSE MULTI-CONTAINER"
    echo "------------------------------------------"
    
    # Create a sample docker-compose.yml
    cat > docker-compose.example.yml << 'EOF'
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - api
  
  api:
    build: ./api
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
EOF
    
    echo "Created docker-compose.example.yml"
    echo ""
    echo "Commands:"
    echo "  docker-compose up              # Start all services"
    echo "  docker-compose up -d           # Start in detached mode"
    echo "  docker-compose down            # Stop and remove"
    echo "  docker-compose logs -f         # View logs"
    echo "  docker-compose ps              # List services"
}

# =============================================================================
# Example 4: Container Networking
# =============================================================================
example_networking() {
    echo ""
    echo "4. CONTAINER NETWORKING"
    echo "------------------------------------------"
    
    cat << 'EOF'
# Create a custom network
docker network create my-network

# Run containers on the same network
docker run -d --name web --network my-network nginx:alpine
docker run -d --name api --network my-network my-api-image

# Containers can now communicate by name
# From api container: curl http://web:80

# Inspect network
docker network inspect my-network

# Connect running container to network
docker network connect my-network container-name

# Disconnect from network
docker network disconnect my-network container-name

# Remove network
docker network rm my-network
EOF
}

# =============================================================================
# Example 5: Volume Management
# =============================================================================
example_volumes() {
    echo ""
    echo "5. VOLUME MANAGEMENT"
    echo "------------------------------------------"
    
    cat << 'EOF'
# Create a named volume
docker volume create my-volume

# List volumes
docker volume ls

# Inspect volume
docker volume inspect my-volume

# Use volume in container
docker run -d -v my-volume:/data alpine

# Bind mount (host directory to container)
docker run -d -v /host/path:/container/path alpine

# Read-only volume
docker run -d -v my-volume:/data:ro alpine

# Remove unused volumes
docker volume prune

# Remove specific volume
docker volume rm my-volume
EOF
}

# =============================================================================
# Example 6: Container Resource Limits
# =============================================================================
example_resource_limits() {
    echo ""
    echo "6. RESOURCE LIMITS"
    echo "------------------------------------------"
    
    cat << 'EOF'
# Limit memory to 512MB
docker run -d --memory="512m" my-app

# Limit CPU to 1.5 cores
docker run -d --cpus="1.5" my-app

# Combined limits
docker run -d \
  --memory="1g" \
  --cpus="2.0" \
  --memory-reservation="512m" \
  my-app

# Set PID limit
docker run -d --pids-limit=100 my-app

# View container stats
docker stats

# Update limits on running container
docker update --memory="2g" container-id
EOF
}

# =============================================================================
# Example 7: Multi-Stage Builds
# =============================================================================
example_multistage_build() {
    echo ""
    echo "7. MULTI-STAGE BUILDS"
    echo "------------------------------------------"
    
    cat > Dockerfile.multistage << 'EOF'
# Build stage
FROM golang:1.21 AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Final stage
FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/
COPY --from=builder /app/main .

EXPOSE 8080
CMD ["./main"]
EOF
    
    echo "Created Dockerfile.multistage"
    echo ""
    echo "Benefits:"
    echo "  - Smaller final image (only runtime dependencies)"
    echo "  - Better security (no build tools in production)"
    echo "  - Faster deployments"
    echo ""
    echo "Build: docker build -f Dockerfile.multistage -t my-go-app ."
}

# =============================================================================
# Example 8: Health Checks
# =============================================================================
example_health_checks() {
    echo ""
    echo "8. HEALTH CHECKS"
    echo "------------------------------------------"
    
    cat << 'EOF'
# Add health check to Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Or in docker run
docker run -d \
  --health-cmd="curl -f http://localhost:8080/health || exit 1" \
  --health-interval=30s \
  --health-timeout=3s \
  --health-retries=3 \
  my-app

# View health status
docker ps  # Shows health in STATUS column

# Inspect health check logs
docker inspect --format='{{json .State.Health}}' container-id | jq
EOF
}

# =============================================================================
# Main Execution
# =============================================================================

main() {
    example_basic_docker
    example_build_image
    example_docker_compose
    example_networking
    example_volumes
    example_resource_limits
    example_multistage_build
    example_health_checks
    
    echo ""
    echo "=========================================="
    echo "All examples generated successfully!"
    echo "=========================================="
    echo ""
    echo "Files created:"
    echo "  - Dockerfile.example"
    echo "  - Dockerfile.multistage"
    echo "  - docker-compose.example.yml"
    echo ""
    echo "Next steps:"
    echo "  1. Review the generated files"
    echo "  2. Customize for your use case"
    echo "  3. Build and test the containers"
    echo ""
}

# Run main function
main
