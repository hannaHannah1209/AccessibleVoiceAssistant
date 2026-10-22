# Accessible AI Voice Assistant — Beginner Setup (Mac)

This Streamlit prototype lets a user record a voice message or type a question, sends it to Google Gemini, and can read the answer aloud on macOS.

## 1. Open Terminal and go to the project folder

In Terminal, use `cd` to enter the folder where you extracted this ZIP. For example:

```bash
cd ~/Downloads/AccessibleVoiceAssistant_Gemini
```

If you extracted it somewhere else, adjust the path.

## 2. Install the packages

Run:

```bash
python3 -m pip install -r requirements.txt
```

If your Mac uses `python` instead of `python3`, use `python -m pip install -r requirements.txt`.

## 3. Create a Gemini API key

1. Open [Google AI Studio API keys](https://aistudio.google.com/apikey).
2. Sign in and create an API key.
3. Copy it. Do not share it or post it on GitHub.

Google's API availability and usage limits can vary by account and region.

## 4. Save the API key privately

In Terminal, while inside the project folder, run:

```bash
mkdir -p .streamlit
open -e .streamlit/secrets.toml
```

A text editor should open. Paste this line, replacing the example value with your real key:

```toml
GEMINI_API_KEY = "PASTE_YOUR_REAL_KEY_HERE"
```

Save the file and close the editor.

**Important:** Do not upload `.streamlit/secrets.toml` to GitHub or share it with anyone.

## 5. Start the app

In Terminal, run:

```bash
python3 -m streamlit run app.py
```

If that command fails because `python3` is not the Python command on your computer, try:

```bash
python -m streamlit run app.py
```

Streamlit should open the app in your web browser.

## 6. Use the app

1. Use **Record a voice message** to record a short question.
2. Wait for the speech recognition to fill in the text box.
3. Check or edit the text.
4. Click **Ask Gemini**.
5. Use **Read answer aloud** to hear the answer on macOS.

You can also type a message directly without recording.

## Troubleshooting

- **Gemini is not connected:** Check that `.streamlit/secrets.toml` is in the same folder as `app.py`, and that the line starts with `GEMINI_API_KEY =`.
- **Invalid API key or Gemini error:** Create/check the key in Google AI Studio, confirm API access, and check your internet connection.
- **Speech not recognized:** Try a shorter recording, speak clearly, or type the message instead.
- **App does not start:** Confirm Terminal is in the folder that contains `app.py`, then reinstall packages with `python3 -m pip install -r requirements.txt`.
- **Port already in use:** Stop the previous Streamlit run with Control+C, then start it again.

This is an educational prototype, not an emergency-response service. Do not rely on it as the only way to get urgent help.
