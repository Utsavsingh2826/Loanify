#!/bin/bash

# LoaniFi - Complete Setup and Run Script

echo "========================================"
echo "LoaniFi - Complete Setup and Run"
echo "========================================"
echo ""

# Step 1: Check for .env file
if [ ! -f .env ]; then
    if [ -f env.template ]; then
        echo "Creating .env file from template..."
        cp env.template .env
        echo ""
        echo "IMPORTANT: Please edit .env and add your OPENAI_API_KEY"
        echo "Then run this script again."
        exit 1
    fi
fi

# Step 2: Kill processes on ports
echo "Step 1: Freeing up ports..."
echo ""

# Kill port 3000 (Frontend)
PORT_3000=$(lsof -ti:3000)
if [ ! -z "$PORT_3000" ]; then
    echo "Terminating process on port 3000..."
    kill -9 $PORT_3000 2>/dev/null
fi

# Kill port 8000 (Backend)
PORT_8000=$(lsof -ti:8000)
if [ ! -z "$PORT_8000" ]; then
    echo "Terminating process on port 8000..."
    kill -9 $PORT_8000 2>/dev/null
fi

echo "Ports freed!"
echo ""

# Step 3: Check Docker
echo "Step 2: Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running!"
    echo "Please start Docker and run this script again."
    exit 1
fi
echo "Docker is running"
echo ""

# Step 4: Stop any existing containers
echo "Step 3: Stopping existing containers..."
docker-compose down > /dev/null 2>&1
echo ""

# Step 5: Start services
echo "Step 4: Starting all services..."
echo "This may take a few minutes..."
echo ""
docker-compose up -d --build

# Wait for services to start
echo ""
echo "Step 5: Waiting for services to be ready..."
sleep 15

# Check health
echo ""
echo "Step 6: Checking service health..."
echo ""

if curl -s http://localhost:8000/health > /dev/null; then
    echo "[OK] Backend is healthy"
else
    echo "[WAIT] Backend is starting..."
fi

if curl -s http://localhost:3000 > /dev/null; then
    echo "[OK] Frontend is healthy"
else
    echo "[WAIT] Frontend is starting..."
fi

echo ""
echo "========================================"
echo "SUCCESS! LoaniFi is now running!"
echo "========================================"
echo ""
echo "Access the application:"
echo ""
echo "  Frontend:    http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs:    http://localhost:8000/docs"
echo "  Admin:       http://localhost:3000/admin"
echo ""
echo "Useful commands:"
echo "  View logs:        docker-compose logs -f"
echo "  Stop services:    docker-compose down"
echo "  Restart backend:  docker-compose restart backend"
echo "  Restart frontend: docker-compose restart frontend"
echo ""

# Try to open in browser (works on macOS and some Linux)
if command -v open > /dev/null; then
    open http://localhost:3000
elif command -v xdg-open > /dev/null; then
    xdg-open http://localhost:3000
fi

echo "Application should open in your browser shortly!"
echo ""


