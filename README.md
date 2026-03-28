# Smart Traffic System with Chatbot

Minimal demo combining:
- Chatbot-like text input
- Heuristic traffic prediction (time-based)
- NetworkX road graph
- Dijkstra route suggestion
- Simple Flask HTML/CSS interface

## Setup

1. Create and activate virtual environment:
   - `python -m venv .venv`
   - Windows: `.venv\Scripts\activate`

2. Install dependencies:
   - `pip install -r requirements.txt`

3. Run app:
   - `python app.py`

4. Open in browser:
   - `http://127.0.0.1:5000`

## Usage

- Query e.g.: `Best route from A to D at 6pm`
- Or `Traffic at 9am`
- You can also set source/destination/time fields

## File map

- `app.py` - Flask web controller
- `chatbot.py` - NLP-simplified parser for intent + slots
- `traffic_predictor.py` - time-based heuristic congestion prediction
- `road_graph.py` - static NetworkX graph and weight updater
- `routing.py` - Dijkstra shortest path
- `response.py` - output formatting
- `templates/index.html` + `static/styles.css` - UI
