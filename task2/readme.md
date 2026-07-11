# 🌀 The Void Console

A playful Streamlit chat app that connects you to different "comms channels" — each powered by a distinct AI personality — using Google's Gemini 2.5-Flash model.

## Features

- **Multiple comms channels**: Talk to Nick Fury (blunt director), J.A.R.V.I.S. (polite AI butler), or the Sorcerer Supreme (mystic riddler).
- **Separate chat histories**: Each channel keeps its own conversation thread.
- **Streaming responses**: Watch the reply arrive in real time, word by word.
- **Status updates**: A live status widget shows "Establishing secure uplink" → "Decrypting..." → "Transmission received."
- **Wipe channel logs**: Clear the current channel's history with one click.

## Demo

![Demo] (image.png)

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
     copy .env.example .env   # Windows CMD
     # or
     cp .env.example .env     # macOS/Linux
     ```
   - Edit `.env` and add your actual Gemini API key:
     ```
     API_KEY=your_actual_gemini_api_key_here
     ```
   - Alternatively, export the variable in your shell:
     ```bash
     setx API_KEY "your_actual_gemini_api_key_here"   # Windows CMD
     # or in PowerShell: $env:API_KEY="your_actual_gemini_api_key_here"
     ```

5. **Run the app**:
   ```bash
   streamlit run app.py
   ```
   The console will open at `http://localhost:8501` (or another port if specified).

## Usage

- Select a comms channel from the dropdown.
- Type your message in the chat box and press Enter.
- Watch the reply stream in with that channel's unique personality.
- Use **Wipe Channel Logs** to reset the conversation for the current channel.

## Custom Personas

Edit the `PERSONAS` dictionary in `app.py`. Each entry maps a channel name to a system-prompt string that defines its tone.

## Extending

- **Add more channels**: Add new entries to the `PERSONAS` dictionary.
- **Change the model**: Replace `"gemini-2.5-flash"` with another Gemini model name if you have access.
- **Persist chats**: Serialize `st.session_state.chat_histories` to a JSON file on disk so conversations survive restarts.
- **Add avatars**: Pass `avatar="path/to/img.png"` to `st.chat_message(...)` for each role.

## Requirements

See `requirements.txt` for exact dependencies.

## License

This project is for educational / demo purposes. Feel free to modify and share.