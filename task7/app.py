import os
import json
import re
import urllib.parse

import dotenv
import pandas as pd
import requests
import streamlit as st
import google.generativeai as genai

# ============================================================
# Setup & Configuration
# ============================================================

dotenv.load_dotenv()
api_key = os.getenv("API_KEY")

st.set_page_config(page_title="Life-OS Dashboard", page_icon="🧠", layout="wide")

if not api_key:
    st.error("`API_KEY` environment variable not set. Add it to your .env file.")
    st.stop()

genai.configure(api_key=api_key)


@st.cache_resource
def get_model():
    return genai.GenerativeModel("gemini-2.5-flash")


# ============================================================
# Phase 1: The Data Pipeline
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv("screentime.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df


df = load_data()

st.title("🧠 Life-OS")
st.write("A brutal-but-fair dashboard for your digital habits.")

# ============================================================
# Phase 2: The Command Center UI — Sidebar Controls
# ============================================================

st.sidebar.header("Command Center")

available_dates = sorted(df["Date"].dt.date.unique())
selected_date = st.sidebar.selectbox(
    "Select Day", options=available_dates, index=len(available_dates) - 1
)

daily_goal_minutes = st.sidebar.slider(
    "Daily Goal (minutes)", min_value=60, max_value=480, value=180, step=15
)
st.sidebar.caption(f"= {daily_goal_minutes // 60}h {daily_goal_minutes % 60}m")

day_df = df[df["Date"].dt.date == selected_date]

# ============================================================
# Phase 2: The KPI Row
# ============================================================

total_minutes_today = int(day_df["Minutes_Used"].sum())

if not day_df.empty:
    app_totals = day_df.groupby("App_Name")["Minutes_Used"].sum()
    most_used_app = app_totals.idxmax()
    most_used_minutes = int(app_totals.max())
else:
    most_used_app = "—"
    most_used_minutes = 0

delta_minutes = total_minutes_today - daily_goal_minutes

col1, col2, col3 = st.columns(3)

with col1:
    hours = total_minutes_today // 60
    mins = total_minutes_today % 60
    st.metric("Total Screen Time Today", f"{hours}h {mins}m")

with col2:
    st.metric("Most Used App", most_used_app, f"{most_used_minutes} min")

with col3:
    st.metric(
        "vs Daily Goal",
        f"{daily_goal_minutes // 60}h {daily_goal_minutes % 60}m goal",
        delta=f"{delta_minutes:+d} min",
        delta_color="inverse",
    )

st.divider()

# ============================================================
# Phase 2: The Visualizations
# ============================================================

viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.subheader("📈 14-Day Trend")
    daily_totals = df.groupby(df["Date"].dt.date)["Minutes_Used"].sum()
    st.line_chart(daily_totals)

with viz_col2:
    st.subheader("📊 Today's Category Breakdown")
    if not day_df.empty:
        category_totals = day_df.groupby("Category")["Minutes_Used"].sum()
        st.bar_chart(category_totals)
    else:
        st.write("No data for this day.")

st.divider()

# ============================================================
# Phase 3: The AI Integration
# ============================================================

st.subheader("🤖 Your Life Coach")


def summarize_day(day_data: pd.DataFrame) -> str:
    """Phase 3, Step 8: The Data Bridge — aggregate minutes per category
    into a clean string Gemini can read."""
    if day_data.empty:
        return "No screen time recorded today."
    category_summary = day_data.groupby("Category")["Minutes_Used"].sum()
    return category_summary.to_string()


def build_prompt(summary_text: str, total_minutes: int, goal_minutes: int) -> str:
    return f"""You are a holistic life coach who is brutal but fair. You do not simply say
"use your phone less" — you analyze the specific categories of usage and suggest concrete,
physical, real-world replacements for the time spent.

Today's screen time by category (in minutes):
{summary_text}

Total screen time today: {total_minutes} minutes.
The user's daily goal: {goal_minutes} minutes.

Respond ONLY with a single valid JSON object, no markdown fences, no extra text, with these
exact keys:
1. "coaching_text": 2-4 sentences of direct, specific coaching. If a category (e.g. Social
   Media or Entertainment) is high, name a specific real-world replacement activity
   (e.g. a 20-minute walk, meal prepping, reading a chapter of a book).
2. "severity": one of "good", "moderate", or "bad", based on how far total screen time is
   from the goal and how much of it was low-value (Social Media/Entertainment) vs
   high-value (Education/Coding).
3. "avatar_prompt": a vivid, visually descriptive AI image prompt representing the user's
   day. For "bad" severity, describe something like a tired, screen-fried figure. For
   "moderate", something neutral. For "good", describe a focused, energized figure.
   Include art style, lighting, and mood in the description.
"""


def parse_json_response(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    return json.loads(cleaned)


def generate_avatar_image(image_prompt: str):
    """Innovation Deliverable: The Guilt-Trip Avatar — renders an image via
    Pollinations reflecting the day's severity, with graceful fallback."""
    encoded_prompt = urllib.parse.quote(image_prompt)
    for model_name in ["turbo", "flux"]:
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&model={model_name}"
        try:
            response = requests.get(url, timeout=45)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException:
            continue
    return None


if st.button("🔍 Analyze My Day"):
    summary_text = summarize_day(day_df)
    prompt = build_prompt(summary_text, total_minutes_today, daily_goal_minutes)

    # --- Graceful failure around the Gemini call ---
    try:
        with st.spinner("Your coach is reviewing your habits..."):
            model = get_model()
            response = model.generate_content(prompt)
            parsed = parse_json_response(response.text)
    except json.JSONDecodeError:
        st.toast("⚠️ Coach response wasn't valid JSON. Please try again.")
        parsed = None
    except Exception as e:
        st.toast(f"⚠️ AI coaching failed: {e}")
        parsed = None

    if parsed:
        coaching_text = parsed.get("coaching_text", "")
        severity = parsed.get("severity", "moderate")
        avatar_prompt = parsed.get("avatar_prompt", "")

        if severity == "bad":
            st.warning(coaching_text)
        elif severity == "good":
            st.success(coaching_text)
        else:
            st.info(coaching_text)

        # --- Graceful failure around the image API ---
        try:
            image_bytes = generate_avatar_image(avatar_prompt)
            if image_bytes:
                st.image(image_bytes, caption="Your day, visualized", width=300)
            else:
                st.toast("🖼️ Image server is busy, skipping visual...")
        except Exception:
            st.toast("🖼️ Image server is busy, skipping visual...")