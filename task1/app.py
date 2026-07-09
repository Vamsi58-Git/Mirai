import streamlit as st

# --- Task 1: The UI Shell ---
st.title("🛡️ V.K. Transmission Console")
st.write("Created and secured by LORD VAMSI KRISHNA ⚡")
st.write("Agent, identify yourself and encode your message below. Hit **Transmit** when ready to beam it to headquarters.")

# --- Task 2: Multi-Data Collection ---
user_name = st.text_input("Agent Codename")
user_message = st.text_input("Encrypted Message")

# --- Task 3: The Action Gate ---
if st.button("🚀 Transmit"):

    # --- Task 4: Conditional Routing (Edge Cases) ---
    if user_name == "":
        st.error("⚠️ Access Denied:  Need your codename before you touch this console.")
    elif user_message == "":
        st.warning("📡 Signal Empty: Even Jarvis can't transmit silence. Type something, Agent.")
    else:
        # --- Task 5: The Formatted Output ---
        st.success(f"✅ Uplink Confirmed! Welcome aboard, Agent {user_name}. Message received: \"{user_message}\"")

        # --- Advanced Challenge: Token Cost Estimator ---
        char_count = len(user_message)
        token_count = char_count // 4 #1 token ≈ 4 characters approximately
        st.info(f"🧠 Vision's Power Scan: This transmission will draw approximately {token_count} tokens of Stark-grade compute from the mainframe.")