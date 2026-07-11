# 🌀 The Void Console (Legacy Version)

A playful Streamlit chat app that connects you to different "comms channels" — each powered by a distinct AI personality — using Google's Gemini 2.5-Flash model.

## Features

- **Multiple comms channels**: Talk to Nick Fury (blunt director), J.A.R.V.I.S. (polite AI butler), or the Sorcerer Supreme (mystic riddler).
- **Single-turn conversation**: Send a message to the active channel and get a direct response. Due to the lack of session history caching, previous messages are not remembered across runs.
- **Standard Input UI**: Simple message input using `st.text_input` and `st.button`.

## Setup

1. **Clone / copy this folder** to your machine.

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
     copy .env.example .env
     ```
   - Edit `.env` and add your actual Gemini API key:
     ```
     API_KEY=your_actual_gemini_api_key_here
     ```

5. **Run the app**:
   ```bash
   streamlit run app.py
   ```
   (Note: To run this legacy version, rename `previous.py` to `app.py` or run `streamlit run previous.py` directly).

## Custom Personas

Edit the `PERSONAS` dictionary in `app.py`. Each entry maps a channel name to a system-prompt string that defines its tone.
