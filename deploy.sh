#!/bin/bash

# SyntaxSage Docker Deployment Script
# This script sets up and runs the complete SyntaxSage application with Gemma3

echo "🧙‍♂️ SyntaxSage Docker Deployment"
echo "=================================="
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed"
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are available"
echo

# Check available system resources
echo "📊 Checking system resources..."
free -h | grep -E "Mem|Swap" || echo "Memory info not available"
echo

# Pull Gemma3 model if not available
echo "📥 Pulling Gemma3 model (this may take a while)..."
docker pull ai/gemma3:4B-Q4_K_M

if [ $? -ne 0 ]; then
    echo "❌ Failed to pull Gemma3 model"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo "✅ Gemma3 model pulled successfully"
echo

# Build and start services
echo "🚀 Building and starting SyntaxSage services..."
docker-compose up --build -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start services"
    echo "Check the logs with: docker-compose logs"
    exit 1
fi

echo "✅ Services started successfully!"
echo

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🏥 Checking service health..."

# Check Gemma3 health
if curl -f http://localhost:8080/health &> /dev/null; then
    echo "✅ Gemma3 API is healthy"
else
    echo "⚠️  Gemma3 API health check failed"
fi

# Check Streamlit health
if curl -f http://localhost:8501/_stcore/health &> /dev/null; then
    echo "✅ Streamlit app is healthy"
else
    echo "⚠️  Streamlit app health check failed"
fi

echo
echo "🎉 SyntaxSage is now running!"
echo
echo "📍 Access points:"
echo "   • Streamlit App: http://localhost:8501"
echo "   • Gemma3 API:   http://localhost:8080"
echo "   • Nginx Proxy:  http://localhost:80"
echo
echo "🔧 Management commands:"
echo "   • View logs:    docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Restart:      docker-compose restart"
echo
echo "📖 Open http://localhost:8501 in your browser to start analyzing code!"