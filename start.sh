#!/bin/bash
# RefactorGPT Startup Script

echo "🚀 Starting RefactorGPT..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Using default settings."
    echo "   Copy .env.example to .env and add your API keys for full functionality."
    echo ""
fi

# Start the server
echo "✅ Starting FastAPI server..."
echo "📍 Web UI: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo "📍 Health Check: http://localhost:8000/health"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
