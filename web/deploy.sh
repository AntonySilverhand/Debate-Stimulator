#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}==== Debate Stimulator Web Application Deployment ====${NC}"
echo ""

# Navigate to project root
cd "$(dirname "$0")"
PROJECT_ROOT=$(pwd)

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed. Please install Node.js 14 or higher.${NC}"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is not installed. Please install npm.${NC}"
    exit 1
fi

# Backend setup
echo -e "${GREEN}Setting up backend...${NC}"
cd "$PROJECT_ROOT/backend"

# Create Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || { echo -e "${RED}Failed to activate virtual environment${NC}"; exit 1; }

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt || { echo -e "${RED}Failed to install backend dependencies${NC}"; exit 1; }

# Start backend server in background
echo "Starting backend server..."
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

echo "Backend server started with PID $BACKEND_PID"
echo "Backend logs will be written to backend.log"

# Wait a moment for the backend to start
sleep 2

# Frontend setup
echo -e "${GREEN}Setting up frontend...${NC}"
cd "$PROJECT_ROOT/frontend"

# Install frontend dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install || { echo -e "${RED}Failed to install frontend dependencies${NC}"; exit 1; }
fi

# Build production version of frontend
echo "Building frontend..."
npm run build || { echo -e "${RED}Failed to build frontend${NC}"; exit 1; }

# Serve frontend using a simple HTTP server
echo "Serving frontend..."
npx serve -s build -l 3000 > frontend.log 2>&1 &
FRONTEND_PID=$!

echo "Frontend server started with PID $FRONTEND_PID"
echo "Frontend logs will be written to frontend.log"

echo ""
echo -e "${GREEN}===== Deployment complete! =====${NC}"
echo -e "${GREEN}Backend API is running at:${NC} http://localhost:8000"
echo -e "${GREEN}Frontend is running at:${NC} http://localhost:3000"
echo ""
echo "To stop the servers, run: kill $BACKEND_PID $FRONTEND_PID"
echo "Press Ctrl+C to stop viewing logs"

# Display logs
echo "Displaying logs (press Ctrl+C to stop)..."
tail -f backend.log frontend.log
