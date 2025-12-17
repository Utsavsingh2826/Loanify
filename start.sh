#!/bin/bash

# LoaniFi Startup Script
# This script helps you get started with the LoaniFi application

echo "🚀 LoaniFi - AI-Powered Loan Chatbot"
echo "===================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your OPENAI_API_KEY"
    echo "   You can get an API key from: https://platform.openai.com/api-keys"
    echo ""
    read -p "Press Enter once you've added your API key to continue..."
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if services are already running
if docker-compose ps | grep -q "Up"; then
    echo "⚠️  Services are already running"
    read -p "Do you want to restart them? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔄 Stopping existing services..."
        docker-compose down
    else
        echo "✅ Keeping existing services running"
        echo ""
        echo "📍 Access the application:"
        echo "   - Frontend: http://localhost:3000"
        echo "   - Backend API: http://localhost:8000"
        echo "   - API Docs: http://localhost:8000/docs"
        echo "   - Admin: http://localhost:3000/admin"
        exit 0
    fi
fi

# Start services
echo "🏗️  Building and starting services..."
echo "   (This may take a few minutes on first run)"
echo ""
docker-compose up -d --build

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check health
echo ""
echo "🔍 Checking service health..."

if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "⚠️  Backend is starting... (may take a moment)"
fi

if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is healthy"
else
    echo "⚠️  Frontend is starting... (may take a moment)"
fi

echo ""
echo "═══════════════════════════════════════"
echo "✅ LoaniFi is now running!"
echo "═══════════════════════════════════════"
echo ""
echo "📍 Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Admin Dashboard: http://localhost:3000/admin"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
echo "🎬 Ready for demo! Check DEMO_GUIDE.md for demo instructions."
echo ""


