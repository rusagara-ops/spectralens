# SpectraLens

AI-powered crop health analysis from hyperspectral drone imagery.

## Quick Start

1. Add your Anthropic API key to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

2. Run:
   ```bash
   bash start.sh
   ```

3. Open http://localhost:5173

## Tech Stack

- **Frontend**: React 18 + Vite + Tailwind CSS + Recharts
- **Backend**: Python + FastAPI + Uvicorn
- **AI**: Anthropic Claude API
- **Data**: NumPy + SciPy + Pillow (synthetic hyperspectral data)
