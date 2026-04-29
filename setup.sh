#!/bin/bash

# AI Personalized Learning Platform - Setup Script
# This script sets up both backend and frontend

set -e

echo "🚀 Starting AI Learning Platform Setup..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Backend Setup
echo -e "${BLUE}Step 1: Setting up Backend...${NC}"

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null || true

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

echo -e "${GREEN}✓ Backend setup complete!${NC}"

# Step 2: Frontend Setup
echo -e "${BLUE}Step 2: Setting up Frontend...${NC}"

cd ../frontend

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file from .env.example..."
    cp .env.example .env.local
fi

# Install dependencies
if [ -x "$(command -v pnpm)" ]; then
    echo "Installing dependencies with pnpm..."
    pnpm install
elif [ -x "$(command -v npm)" ]; then
    echo "Installing dependencies with npm..."
    npm install
else
    echo "Error: pnpm or npm not found"
    exit 1
fi

echo -e "${GREEN}✓ Frontend setup complete!${NC}"

# Step 3: Summary
echo ""
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Start Backend:"
echo "   cd backend"
echo "   python main.py"
echo ""
echo "2. Start Frontend (in another terminal):"
echo "   cd frontend"
echo "   pnpm dev"
echo ""
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo -e "${YELLOW}API Documentation: http://192.168.0.131:8001/api/docs${NC}"
