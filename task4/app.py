import random
import urllib.parse
import streamlit as st

# --- Page Setup ---
st.title("🎨 AI Image Studio")
st.write("Describe anything you can imagine, pick a style, and let the AI paint it for you.")

# --- Sidebar Settings ---
st.sidebar.header("Settings")

art_style = st.sidebar.selectbox(
    "Art Style",
    ["Realistic", "Anime", "Cyberpunk", "Watercolor", "Oil Painting"],
)

width = st.sidebar.slider("Width", min_value=256, max_value=1024, value=512, step=64)
height = st.sidebar.slider("Height", min_value=256, max_value=1024, value=512, step=64)

speed_mode = st.sidebar.radio(
    "Generation Mode",
    ["⚡ Fast (turbo)", "🎨 Quality (flux)"],
    index=0,
)
model_name = "turbo" if "Fast" in speed_mode else "flux"

magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

# --- Surprise Me Prompt Bank (Task 4) ---
SURPRISE_PROMPTS = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon sipping coffee in a cozy cafe",
    "A underwater city powered by bioluminescent jellyfish",
    "A robot painting a self-portrait in a Renaissance studio",
]

# --- Main Prompt Input ---
prompt = st.text_input("Describe your image")

generate_clicked = st.button("Generate Image")
surprise_clicked = st.button("🎲 Surprise Me!")


def build_and_show_image(base_prompt: str):
    """Builds the final prompt (with optional Magic Enhance), calls the
    image API with width/height, displays the image, and offers a download."""

    full_prompt = f"{base_prompt}, {art_style} style"

    # --- Task 3: Magic Enhance Toggle ---
    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    # URL-encode the prompt so spaces/commas don't break the request
    encoded_prompt = urllib.parse.quote(full_prompt)

    import requests
    import time

    # Try the selected model first, then fall back to the other one if it fails.
    models_to_try = [model_name, "flux" if model_name == "turbo" else "turbo"]

    per_attempt_timeout = 45
    image_bytes = None
    last_error = None

    with st.spinner(f"Generating with {model_name}... usually 10-30 seconds."):
        for try_model in models_to_try:
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model={try_model}"
            try:
                response = requests.get(url, timeout=per_attempt_timeout)
                response.raise_for_status()
                image_bytes = response.content
                if try_model != model_name:
                    st.caption(f"Note: '{model_name}' was unavailable, used '{try_model}' instead.")
                break
            except requests.exceptions.RequestException as e:
                last_error = e
                time.sleep(1)

    if image_bytes:
        st.image(image_bytes, caption=full_prompt)

        # --- Task 2: Fixed File Extension + Dynamic Filename ---
        st.download_button(
            label="Download Image",
            data=image_bytes,
            file_name=f"{art_style}_image.png",
            mime="image/png",
        )
    else:
        st.error(
            f"Image generation failed on both 'turbo' and 'flux' models: {last_error}\n\n"
            "This can happen for a few reasons:\n"
            "- The prompt names a real, identifiable public figure, which some models reject.\n"
            "- Pollinations' servers are temporarily overloaded across models.\n\n"
            "Try a simpler prompt, or wait a minute and try again."
        )


# --- Generate Button Logic ---
if generate_clicked:
    if not prompt:
        st.error("Please enter a prompt first.")
    else:
        build_and_show_image(prompt)

# --- Task 4: Surprise Me Button Logic ---
if surprise_clicked:
    random_prompt = random.choice(SURPRISE_PROMPTS)
    st.info(f"Surprise prompt: {random_prompt}")
    build_and_show_image(random_prompt)