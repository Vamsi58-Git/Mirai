# AI Image Studio

A Streamlit app that turns text prompts into AI-generated images using the free [Pollinations.ai](https://pollinations.ai) API with no API key or signup required.

## Features

- **Prompt-to-image generation**: Describe anything and get an AI-rendered image back.
- **Art style picker**: Choose Realistic, Anime, Cyberpunk, Watercolor, or Oil Painting.
- **Working size controls**: Width and height sliders resize the generated image through URL parameters.
- **Magic Enhance toggle**: Automatically appends quality-boosting keywords to your prompt.
- **Surprise Me button**: Instantly generates an image from a bank of random creative prompts.
- **Fast/Quality mode**: Switch between the `turbo` model and `flux` model.
- **Automatic model fallback**: If your selected model is temporarily down, the app retries with the other one.
- **Working downloads**: Downloaded images are saved as real `.png` files.

## Setup

1. **Clone or copy this folder** to your machine.
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
   The app will open at `http://localhost:8501` or another port if specified.

No API key setup is needed because Pollinations' free tier is used by default.

## Usage

1. Type a description in **Describe your image**.
2. Optionally adjust the **Art Style**, **Width/Height**, **Generation Mode**, and **Magic Enhance** settings in the sidebar.
3. Click **Generate Image** or **Surprise Me!**.
4. Once the image appears, click **Download Image** to save it as a `.png`.

## Notes on Reliability

Pollinations is a free, community-run API and can occasionally be slow or return errors on a given model. This app handles that by:

- Trying your selected model first, then automatically falling back to the other model if needed.
- Showing a clear error message if both models fail.
- Explicitly pinning to known working models (`turbo`, `flux`).

Prompts naming real, identifiable public figures may be rejected by the underlying model's content-safety filters.

## Requirements

See `requirements.txt` for exact dependencies.

## License

This project is for educational and demo purposes. Feel free to modify and share.
