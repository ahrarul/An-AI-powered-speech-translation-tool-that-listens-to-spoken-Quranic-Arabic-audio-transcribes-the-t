import os
import sqlite3
import streamlit as st
from openai import OpenAI
from gtts import gTTS
import base64

# --- Page Layout Configuration ---
st.set_page_config(page_title="AI Quran Speech Translator", page_icon="📖", layout="centered")
st.title("📖 AI Quran Recitation Translation Agent")
st.write("Record or upload an Arabic Quranic recitation to transcribe and translate it.")

# --- Initialize AI Clients ---
# Hugging Face safely reads OPENAI_API_KEY from your Space Repository Secret settings
client = OpenAI()

# --- Database Query Helper ---
def get_verse_translation(surah, ayah):
    try:
        conn = sqlite3.connect('quran.db')
        cursor = conn.cursor()
        # Modify table name 'verses' or column names to match your exact quran.db layout
        cursor.execute("SELECT arabic_text, english_translation FROM verses WHERE surah=? AND ayah=?", (surah, ayah))
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        return None

# --- Main Web UI Application Logic ---
# 1. Provide an audio file uploader tool (replaces live microphone files in browser)
uploaded_file = st.file_uploader("Upload your recitation file (.wav format)", type=["wav"])

if uploaded_file is not None:
    # Save the file temporarily as input.wav for processing
    with open("input.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.audio("input.wav", format="audio/wav")

    if st.button("✨ Transcribe & Translate Verse"):
        with st.spinner("Processing audio with OpenAI Whisper..."):
            try:
                # 2. Transcribe audio file using OpenAI Whisper ASR
                with open("input.wav", "rb") as audio_data:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_data
                    )
                
                detected_text = transcription.text
                st.success(f"**Transcribed Arabic Text:** {detected_text}")

                # 3. Simulate parsing or matching your database verse text 
                # (For demo: pulling Surah 1, Ayah 1. Update this to dynamic search matching)
                verse_data = get_verse_translation(1, 1)

                if verse_data:
                    arabic_verse, translation_text = verse_data
                    
                    # Display matching outputs in structured layouts
                    st.info(f"**Matched Database Verse:** {arabic_verse}")
                    st.subheader(f"📝 English Translation")
                    st.write(translation_text)

                    # 4. Generate Text-to-Speech Translation Playback (replaces Pygame Mixer)
                    tts = gTTS(text=translation_text, lang='en')
                    tts.save("translation.mp3")
                    
                    # Stream audio natively inside the web user browser interface
                    st.audio("translation.mp3", format="audio/mp3")
                else:
                    st.warning("Audio transcribed successfully, but couldn't find a matching record in quran.db.")

            except Exception as e:
                st.error(f"An error occurred during execution: {e}")
