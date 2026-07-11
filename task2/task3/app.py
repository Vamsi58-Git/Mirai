import os
import dotenv
import streamlit as st
import google.generativeai as genai

dotenv.load_dotenv(override=True)
api_key = os.getenv("API_KEY")
if not api_key:
    st.error("`API_KEY` environment variable not set.")
    st.stop()

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

if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}
if selected_persona not in st.session_state.chat_histories:
    st.session_state.chat_histories[selected_persona] = []

for msg in st.session_state.chat_histories[selected_persona]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Transmit your message..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_histories[selected_persona].append(
        {"role": "user", "content": prompt}
    )

    system_instruction = PERSONAS[selected_persona]
    history_text = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in st.session_state.chat_histories[selected_persona]
    )
    full_prompt = f"{system_instruction}\n\nConversation so far:\n{history_text}\n\nAssistant:"

    try:
        with st.status("📡 Establishing secure uplink...", expanded=False) as status:
            status.update(label="🧠 Decrypting and processing transmission...")
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(full_prompt, stream=True)

            answer_placeholder = st.empty()
            full_answer = ""
            for chunk in response:
                if chunk.text:
                    full_answer += chunk.text
                    answer_placeholder.markdown(full_answer)

            status.update(label="✅ Transmission received.", state="complete")

        st.session_state.chat_histories[selected_persona].append(
            {"role": "assistant", "content": full_answer}
        )
    except Exception as e:
        st.error(f"⚠️ Uplink failure: {e}")

if st.button("🧹 Wipe Channel Logs"):
    st.session_state.chat_histories[selected_persona] = []
    st.rerun()