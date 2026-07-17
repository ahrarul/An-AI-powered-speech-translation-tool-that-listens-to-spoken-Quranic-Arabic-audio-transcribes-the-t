import os
import sqlite3
import streamlit as st
from openai import OpenAI
from gtts import gTTS

# --- Page Layout Configuration ---
st.set_page_config(page_title="AI Quran Speech Translator", page_icon="📖", layout="centered")
st.title("📖 AI Quran Recitation Translation Agent")
st.write("Record or upload an Arabic Quranic recitation to transcribe and translate it.")

# --- Initialize OpenAI Client ---
client = OpenAI()

# --- Language Configuration Map ---
LANGUAGES = {
    "English": "en",
    "Hindi (हिंदी)": "hi",
    "Bengali (বাংলা)": "bn"
}

# --- Database Query Helper ---
def get_verse_arabic(surah, ayah):
    try:
        conn = sqlite3.connect('quran.db')
        cursor = conn.cursor()
        # Grabs just the original Arabic text from your local db
        cursor.execute("SELECT arabic_text FROM verses WHERE surah=? AND ayah=?", (surah, ayah))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        return None

# --- AI Translator Helper ---
def translate_text_with_ai(text, target_language):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are an expert Islamic scholar and linguistics translator. Translate the following Quranic Arabic verse text accurately into {target_language}. Provide only the direct translation text context without preamble or commentary."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Translation processing error: {e}"

# --- Language Selector Dropdown ---
selected_lang_name = st.selectbox("🌐 Choose Translation Language:", list(LANGUAGES.keys()))
target_lang_code = LANGUAGES[selected_lang_name]

# --- Audio File Uploader Tool ---
uploaded_file = st.file_uploader("Upload your recitation file (.wav format)", type=["wav"])

if uploaded_file is not None:
    with open("input.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.audio("input.wav", format="audio/wav")

    if st.button("✨ Transcribe & Translate Verse"):
        with st.spinner("Processing audio with OpenAI Whisper..."):
            try:
                # 1. Transcribe audio file using OpenAI Whisper ASR
                with open("input.wav", "rb") as audio_data:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_data
                    )
                
                detected_text = transcription.text
                st.success(f"**Transcribed Arabic Text:** {detected_text}")

                # 2. Query your local database for original Arabic verse text
                # (Pulling Surah 1, Ayah 1 for demo purposes. Swap with dynamic selection matching later)
                arabic_verse = get_verse_arabic(1, 1)

                if arabic_verse:
                    st.info(f"**Matched Database Verse:** {arabic_verse}")
                    
                    # 3. Dynamic Real-time translation via OpenAI
                    with st.spinner(f"Translating to {selected_lang_name}..."):
                        translation_text = translate_text_with_ai(arabic_verse, selected_lang_name)
                    
                    st.subheader(f"📝 {selected_lang_name} Translation")
                    st.write(translation_text)

                    # 4. Generate dynamic Text-to-Speech matched to translation accent
                    tts = gTTS(text=translation_text, lang=target_lang_code)
                    tts.save("translation.mp3")
                    st.audio("translation.mp3", format="audio/mp3")
                else:
                    st.warning("Audio transcribed, but couldn't locate matching record in quran.db.")

            except Exception as e:
                st.error(f"An error occurred during execution: {e}")
