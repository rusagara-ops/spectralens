#!/bin/bash
echo ""
echo "  SpectraLens — AI-powered crop health analysis"
echo "  ================================================"
echo ""

# Check for API key
if grep -q "your_key_here" "$(dirname "$0")/.env" 2>/dev/null; then
  echo "  WARNING: ANTHROPIC_API_KEY not set in .env"
  echo "  AI analysis will not work until you add your key."
  echo ""
fi

# Install backend dependencies
echo "  Installing backend dependencies..."
cd "$(dirname "$0")/backend"
python3 -m pip install -r requirements.txt -q 2>&1 | tail -1

# Start backend in background
echo "  Starting backend server..."
python3 -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Install and start frontend
echo "  Installing frontend dependencies..."
cd ../frontend
npm install --silent 2>&1 | tail -1

echo "  Starting frontend dev server..."
npm run dev &
FRONTEND_PID=$!

# Wait for servers to start
sleep 3

echo ""
echo "  SpectraLens is running!"
echo "  ────────────────────────────────────"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  API docs: http://localhost:8000/docs"
echo "  ────────────────────────────────────"
echo ""
echo "  Press Ctrl+C to stop."
echo ""

# Wait and clean up
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo ''; echo '  SpectraLens stopped.'; exit 0" EXIT INT TERM
wait
