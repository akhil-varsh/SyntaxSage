#!/bin/bash

# SyntaxSage - AI Code Analysis Tool
# Startup script for Linux/Mac

echo "========================================"
echo "  SyntaxSage - AI Code Analysis Tool"  
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://python.org"
    exit 1
fi

# Check if Ollama is running
echo "Checking Ollama connection..."
if ! curl -s http://localhost:11434/api/version &> /dev/null; then
    echo "WARNING: Ollama might not be running"
    echo "Please ensure Ollama is installed and running with:"
    echo "  ollama serve"
    echo "  ollama pull llama3.1"
    echo
    read -p "Press Enter to continue anyway..."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Start the application
echo
echo "Starting SyntaxSage..."
echo "Application will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo

python app.py