import os
import platform
import subprocess
from io import BytesIO

import streamlit as st
import speech_recognition as sr
from google import genai


st.set_page_config(
    page_title="Accessible AI Voice Assistant",
    page_icon="🎙️",
    layout="centered",
)

st.title("🎙️ Accessible AI Voice Assistant")
st.write(
    "Ask questions by speaking or typing. The assistant uses Google Gemini "
    "to generate answers and can read answers aloud on macOS."
)

def get_gemini_key():
    """Read the Gemini key from Streamlit secrets or an environment variable."""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    return key or os.getenv("GEMINI_API_KEY", "")


def get_ai_reply(user_message):
    """Send a message to Gemini and return its answer."""
    api_key = get_gemini_key()

    if not api_key:
        return (
            "Gemini is not connected yet. Add GEMINI_API_KEY to "
            ".streamlit/secrets.toml, then restart the app."
        )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=(
                "You are a friendly, accessible voice assistant. "
                "Give clear, respectful, easy-to-understand answers. "
                "If the user needs medical, legal, or emergency help, "
                "encourage them to contact a qualified person or local emergency service. "
                "User message: " + user_message
            ),
        )
        answer = getattr(response, "text", None)
        if answer:
            return answer
        return "Gemini did not return a text answer. Please try asking another way."
    except Exception as exc:
        return (
            "I could not connect to Gemini. Check that your API key is correct, "
            "your internet connection works, and your Gemini API access is enabled. "
            f"Technical detail: {exc}"
        )



def speak_text(text_to_speak):
    import json
    import streamlit.components.v1 as components

    safe_text = json.dumps(text_to_speak)

    components.html(
        f"""
        <button id="speakButton"
            style="font-size:16px;padding:12px 18px;cursor:pointer;">
            🔊 Play answer
        </button>

        <script>
        const answerText = {safe_text};
        const button = document.getElementById("speakButton");
        let speaking = false;

        button.onclick = function() {{
            if (!("speechSynthesis" in window)) {{
                alert("Speech is not supported by this browser.");
                return;
            }}

            if (speaking) {{
                window.speechSynthesis.pause();
                speaking = false;
                button.textContent = "▶️ Resume reading";
            }} else if (window.speechSynthesis.paused) {{
                window.speechSynthesis.resume();
                speaking = true;
                button.textContent = "⏸️ Pause reading";
            }} else {{
                window.speechSynthesis.cancel();

                const message = new SpeechSynthesisUtterance(answerText);
                message.lang = "en-US";

                message.onstart = function() {{
                    speaking = true;
                    button.textContent = "⏸️ Pause reading";
                }};

                message.onend = function() {{
                    speaking = false;
                    button.textContent = "🔊 Play answer";
                }};

                message.onerror = function() {{
                    speaking = false;
                    button.textContent = "🔊 Play answer";
                }};

                window.speechSynthesis.speak(message);
            }}
        }};
        </script>
        """,
        height=65,
    )



st.subheader("1. Ask using your voice")
st.caption("Click the microphone, record your message, then submit it below.")
audio_file = st.audio_input("Record a voice message")

recognized_text = ""
if audio_file is not None:
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(BytesIO(audio_file.getvalue())) as source:
            audio_data = recognizer.record(source)
        with st.spinner("Recognizing speech..."):
            recognized_text = recognizer.recognize_google(audio_data)
        st.success("Speech recognized! You can edit the words below.")
    except sr.UnknownValueError:
        st.warning("I could not understand that recording. Please try again or type your message.")
    except sr.RequestError:
        st.warning("Speech recognition could not be reached. Check your internet connection.")
    except Exception as exc:
        st.warning(
            "I could not process that recording. You can type your message below. "
            f"Technical detail: {exc}"
        )

st.subheader("2. Or type your message")
with st.form("message_form"):
    user_message = st.text_area(
        "Your message",
        value=recognized_text,
        placeholder="For example: Explain how to use this voice assistant.",
        height=110,
    )
    submitted = st.form_submit_button("Ask Gemini", use_container_width=True)

if "assistant_answer" not in st.session_state:
    st.session_state["assistant_answer"] = ""

if submitted:
    if not user_message.strip():
        st.warning("Please record or type a message first.")
    else:
        with st.spinner("Gemini is preparing an answer..."):
            st.session_state["assistant_answer"] = get_ai_reply(user_message.strip())

if st.session_state["assistant_answer"]:
    answer = st.session_state["assistant_answer"]
    st.subheader("Gemini's answer")
    st.write(answer)
    if answer.startswith("I could not connect") or answer.startswith("Gemini is not connected"):
        st.info("Once the API key is connected, restart the app and try again.")
    else:
        if st.button("🔊 Read answer aloud"):
            speak_text(answer)

with st.expander("How to connect Gemini"):
    st.markdown(
        """
        1. Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/apikey).
        2. In the folder containing `app.py`, create a folder named `.streamlit`.
        3. Inside it, create a file named `secrets.toml`.
        4. Put this line in the file, replacing the example text with your own key:

           `GEMINI_API_KEY = "PASTE_YOUR_KEY_HERE"`

        5. Save the file and restart the app.

        Keep your API key private. Do not upload `secrets.toml` to GitHub.
        """
    )

st.caption("Prototype note: Speech recognition uses an internet service. Gemini answers require a working API key.")
