# 🎨 AI Image Studio

A Streamlit app that turns text prompts into AI-generated images using the free [Pollinations.ai](https://pollinations.ai) API — no API key or signup required.

## Features

- **Prompt-to-image generation**: Describe anything and get an AI-rendered image back.
- **Art style picker**: Choose Realistic, Anime, Cyberpunk, Watercolor, or Oil Painting.
- **Working size controls**: Width and height sliders that actually resize the generated image (via `?width=` and `?height=` URL parameters).
- **Magic Enhance toggle**: Automatically appends quality-boosting keywords (`masterpiece, 8k resolution, highly detailed...`) to your prompt.
- **Surprise Me button**: Instantly generates an image from a bank of 5 random creative prompts if you have writer's block.
- **Fast/Quality mode**: Switch between the `turbo` model (faster) and `flux` model (higher quality).
- **Automatic model fallback**: If your selected model is temporarily down, the app automatically retries with the other one before failing.
- **Working downloads**: Downloaded images are named after the art style (e.g. `Cyberpunk_image.png`) and open correctly as real `.png` files.

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

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```
   The app will open at `http://localhost:8501` (or another port if specified).

No API key setup is needed — Pollinations' free tier is used by default.

## Usage

1. Type a description in **"Describe your image"**.
2. (Optional) Adjust the **Art Style**, **Width/Height**, **Generation Mode**, and **Magic Enhance** in the sidebar.
3. Click **Generate Image** — or click **🎲 Surprise Me!** to skip straight to a random prompt.
4. Once the image appears, click **Download Image** to save it as a `.png`.

## Notes on Reliability

Pollinations is a free, community-run API and can occasionally be slow or return errors on a given model. This app handles that by:
- Trying your selected model first, then automatically falling back to the other model if needed.
- Showing a clear error message (rather than a silent failure) if both models fail.
- Explicitly pinning to known-working models (`turbo`, `flux`) rather than letting the API auto-select a model that may require paid credits.

Prompts naming real, identifiable public figures (e.g. celebrities, athletes) may be rejected by the underlying model's content-safety filters — this is expected behavior, not a bug.

## Requirements

See `requirements.txt` for exact dependencies.

## License

This project is for educational / demo purposes. Feel free to modify and share.
