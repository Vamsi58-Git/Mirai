import os
import dotenv
import streamlit as st
import google.generativeai as genai

dotenv.load_dotenv(override=True)
api_key = os.getenv("API_KEY")
if not api_key:
    st.error("`API_KEY` environment variable not set.")
    st.stop()

# Configure API
genai.configure(api_key=api_key)

st.title("🌀 The Void Console")
st.write("Choose your comms channel, Agent. Every line is monitored by a different personality on the other end.")

PERSONAS = {
    "Nick Fury (Director Mode)": (
        "You are a no-nonsense spy agency director. Answer with blunt authority, "
        "battle-worn wisdom, and zero patience for excuses. You call the user 'Agent'. "
        "Always ensure your explanations are clear, simple, and direct. Respect any formatting "
        "or brevity requested in the user's prompt."
    ),
    "J.A.R.V.I.S. (AI Assistant)": (
        "You are a hyper-polite, dry-witted AI butler. Answer with impeccable manners, "
        "clever deadpan humor, and the occasional gentle jab at the user's decisions. "
        "Make sure your explanations and answers are simple, structured, and easy to understand. "
        "Align the complexity and length of your response to the user's prompt."
    ),
    "Sorcerer Supreme (Mystic Mode)": (
        "You are a mystical arts master who speaks with dimensional metaphors and "
        "cryptic warnings about the multiverse, but you must always translate these into a "
        "very clear, simple, and easy-to-understand response in plain terms. "
        "Respect the exact formatting or brevity requested in the user's prompt."
    ),
}

selected_persona = st.selectbox("Choose your Comms Channel:", options=list(PERSONAS.keys()), index=0)

user_input = st.text_input("Transmit your message...")
send_button = st.button("SEND")

if send_button and user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    
    system_instruction = PERSONAS[selected_persona]
    full_prompt = f"{system_instruction}\n\nUser: {user_input}\n\nAssistant:"
    
    try:
        with st.status("📡 Establishing secure uplink...", expanded=False) as status:
            status.update(label="🧠 Decrypting and processing transmission...")
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(full_prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                
            status.update(label="✅ Transmission received.", state="complete")
    except Exception as e:
        st.error(f"⚠️ Uplink failure: {e}")
