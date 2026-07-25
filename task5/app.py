import os
import json
import re
import urllib.parse

import dotenv
import requests
import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

# ============================================================
# Phase 1: The Director's Cut (UI & Configuration)
# ============================================================

dotenv.load_dotenv()
api_key = os.getenv("API_KEY")

st.set_page_config(page_title="AI Visual Novel", page_icon="📖")

if not api_key:
    st.error("`API_KEY` environment variable not set. Add it to your .env file.")
    st.stop()

genai.configure(api_key=api_key)


@st.cache_resource
def get_model(system_prompt: str):
    """Caches the Gemini model client so it isn't recreated on every rerun."""
    return genai.GenerativeModel("gemini-2.5-flash", system_instruction=system_prompt)


st.title("📖 AI Visual Novel")
st.write("A choose-your-own-adventure engine, narrated and illustrated by AI in real time.")

st.sidebar.header("Story Settings")
story_genre = st.sidebar.selectbox(
    "Story Genre",
    ["Fantasy Adventure", "Sci-Fi Thriller", "Cozy Mystery", "Post-Apocalyptic Survival", "Fairy Tale"],
)
art_style = st.sidebar.selectbox(
    "Art Style",
    ["Realistic", "Anime", "Watercolor", "Cyberpunk", "Storybook Illustration"],
)

# --- Session State Initialization ---
if "scene" not in st.session_state:
    st.session_state.scene = None          # parsed JSON dict of current scene
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None
if "chat" not in st.session_state:
    st.session_state.chat = None
if "current_config" not in st.session_state:
    st.session_state.current_config = None


# ============================================================
# Phase 2: The Structured JSON Engine
# ============================================================

SYSTEM_PROMPT = """You are a visual novel narrator and game master.

You must respond ONLY with a single valid JSON object, with no markdown fences,
no commentary, and no text outside the JSON. The JSON object must have exactly
these three keys:

1. "story_text": A short, vivid narrative paragraph (3-5 sentences) continuing the story.
2. "image_prompt": A heavily descriptive, visually detailed prompt suitable for an
   AI image generator, describing the current scene. Include art style, lighting,
   composition, and mood.
3. "options": A JSON array of 2 to 3 short, distinct strings representing the choices
   the reader can make next.

Never include any text before or after the JSON object.
"""


def parse_json_response(raw_text: str) -> dict:
    """Cleans and parses Gemini's response into a Python dict, tolerating
    accidental markdown fences around the JSON."""
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    return json.loads(cleaned)


# ============================================================
# Phase 4 (part): Image + Audio generation helpers
# ============================================================

def generate_image(image_prompt: str, style: str):
    """Fetches an image from Pollinations. Returns bytes, or None on failure."""
    full_prompt = f"{image_prompt}, {style} style"
    encoded_prompt = urllib.parse.quote(full_prompt)
    models_to_try = ["turbo", "flux"]

    for model_name in models_to_try:
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=512&model={model_name}"
        try:
            response = requests.get(url, timeout=45)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException:
            continue

    return None


def generate_audio(text: str):
    """Converts story_text to speech using gTTS. Returns bytes, or None on failure."""
    try:
        tts = gTTS(text=text, lang="en")
        buffer = io.BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        return None


# ============================================================
# Core turn-advancing logic (used by both "Start" and choice buttons)
# ============================================================

def advance_story(user_action: str):
    """Sends the user's action to Gemini, parses the JSON response, and
    generates the accompanying image and narration. Wrapped in graceful
    failure handling throughout (Phase 5)."""

    # --- Phase 5: Graceful failure around the Gemini call itself ---
    try:
        raw_response = st.session_state.chat.send_message(user_action)
        parsed = parse_json_response(raw_response.text)
    except json.JSONDecodeError:
        st.toast("⚠️ The AI's response wasn't valid JSON. Please try again.")
        return
    except Exception as e:
        st.toast(f"⚠️ Story generation failed: {e}")
        return

    st.session_state.scene = parsed

    # --- Phase 5: Graceful failure around the image API ---
    try:
        image_bytes = generate_image(parsed.get("image_prompt", ""), art_style)
        if image_bytes is None:
            st.toast("🖼️ Image server is busy, skipping visual...")
        st.session_state.image_bytes = image_bytes
    except Exception:
        st.toast("🖼️ Image server is busy, skipping visual...")
        st.session_state.image_bytes = None

    # --- Phase 5: Graceful failure around TTS ---
    try:
        audio_bytes = generate_audio(parsed.get("story_text", ""))
        if audio_bytes is None:
            st.toast("🔇 Narration unavailable, continuing silently...")
        st.session_state.audio_bytes = audio_bytes
    except Exception:
        st.toast("🔇 Narration unavailable, continuing silently...")
        st.session_state.audio_bytes = None


# ============================================================
# Start / Restart Controls
# ============================================================

config_now = (story_genre, art_style)

if st.session_state.scene is None:
    st.info("Choose your Genre and Art Style in the sidebar, then start your adventure.")
    if st.button("🚀 Start Adventure"):
        model = get_model(SYSTEM_PROMPT)
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.current_config = config_now
        advance_story(
            f"Begin a new {story_genre} story. Set the opening scene and give the reader their first choices."
        )
        st.rerun()

else:
    if st.sidebar.button("🔄 Restart Story"):
        st.session_state.scene = None
        st.session_state.image_bytes = None
        st.session_state.audio_bytes = None
        st.session_state.chat = None
        st.rerun()

    # ============================================================
    # Phase 4: Multi-Media Rendering (persisted via session_state)
    # ============================================================

    scene = st.session_state.scene

    if st.session_state.image_bytes:
        st.image(st.session_state.image_bytes, use_container_width=True)

    st.write(scene.get("story_text", ""))

    if st.session_state.audio_bytes:
        st.audio(st.session_state.audio_bytes, format="audio/mp3")

    # ============================================================
    # Phase 3: Dynamic UI Generation
    # ============================================================

    st.write("**What do you do?**")
    options = scene.get("options", [])

    for i, option_text in enumerate(options):
        if st.button(option_text, key=f"option_{i}"):
            advance_story(option_text)
            st.rerun()