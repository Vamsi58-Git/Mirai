# 🧠 Life-OS Wellbeing Dashboard

A Streamlit dashboard that visualizes 14 days of screen time data and uses Google's Gemini API as a brutal-but-fair personal life coach — complete with a dynamic "guilt-trip avatar" that visually reflects how your day went.

## Features

- **Synthetic screen time dataset**: 14 days of realistic usage data across 10 apps and 4 categories (`screentime.csv`).
- **Command Center sidebar**: Pick any day to inspect, and set a personal daily screen time goal.
- **KPI row**: Total screen time today, most-used app, and a delta showing how far over/under your goal you are (colored inversely — going over your goal shows red).
- **Trend + breakdown charts**: A 14-day line chart of total usage, and a same-day bar chart broken down by category.
- **AI life coach**: Gemini reads a summarized version of the day's category totals and returns specific, real-world replacement suggestions (not just "use your phone less").
- **Guilt-Trip Avatar**: Gemini also generates an image prompt reflecting the day's severity (good/moderate/bad), which is rendered via Pollinations — a tired figure on bad days, a focused one on good days.
- **Graceful failure handling**: If the AI response isn't valid JSON, or the image API is down, the app shows a toast and keeps working instead of crashing.

## Setup

1. **Clone / copy this folder** to your machine (make sure `screentime.csv` comes with it).

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your Google AI API key**:
   - Copy the example file and rename it to `.env`:
     ```bash
     copy .env.example .env   # Windows CMD
     # or
     cp .env.example .env     # macOS/Linux
     ```
   - Edit `.env` and add your actual Gemini API key.

5. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Pick a day from the sidebar and set your daily goal.
2. Review the KPI row and charts for that day.
3. Click **🔍 Analyze My Day** to get AI coaching and your guilt-trip avatar.

## How It Works

- **Data Bridge**: `summarize_day()` aggregates the day's minutes by category and converts it to a plain string with `.to_string()` — this is what actually gets sent to Gemini, not the raw DataFrame.
- **Structured JSON**: The system prompt forces Gemini to return `coaching_text`, `severity`, and `avatar_prompt` as strict JSON, parsed with `json.loads()`.
- **Severity-based rendering**: `st.warning`/`st.info`/`st.success` are chosen based on the `severity` field the AI itself assigns.
- **Avatar generation**: reuses the turbo→flux fallback pattern from the Image Studio project for resilience against Pollinations outages.

## Deployment

To deploy on Streamlit Community Cloud:
1. Push this repo (including `screentime.csv`, excluding `.env`) to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect your repo, and set `app.py` as the entry point.
3. Add `API_KEY` as a secret in the app's settings (not in the repo).

## Requirements

See `requirements.txt` for exact dependencies.

## License

This project is for educational / demo purposes. Feel free to modify and share.
