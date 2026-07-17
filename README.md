# 📖 Quran Verses AI Speech Translator

An AI-powered speech translation tool that listens to spoken Quranic Arabic audio, transcribes the text, and matches it with official translations from a local database.

---

## 📂 Project Structure

Here is the breakdown of the files in this repository:

*   **`app.py`** – The main entry point of the application. It handles the primary execution flow, coordinates audio input, triggers the AI transcription, and prints or displays the final translation.
*   **`file1.py`** – A utility script containing helper functions, backend logic, and API wrappers (such as OpenAI Whisper or Google Speech-to-Text configurations).
*   **`quran.db`** – A local SQLite database containing the Arabic text of the Quran alongside its multi-language translations, surah names, and ayah numbers.
*   **`input.wav`** – A static, pre-recorded audio sample used as a test file to verify the transcription pipeline without using a microphone.
*   **`live_input.wav`** – A temporary audio cache file generated dynamically when recording real-time speech from the user's microphone.

---

## 🛠️ How It Works

1. **Audio Capture:** The app records live audio via `live_input.wav` or reads from the test file `input.wav`.
2. **AI Transcription:** `file1.py` processes the audio through an Automatic Speech Recognition (ASR) model to extract the Arabic text.
3. **Database Match:** The app queries `quran.db` using the transcribed text to find the exact Surah and Ayah.
4. **Output Display:** `app.py` displays the official Arabic verse alongside its corresponding translation.

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com
cd YOUR_REPO_NAME
pip install -r requirements.txt
```

### 2. Running the Application
To run the speech translator using your default configuration:
```bash
python app.py
```

---

## 📜 License
This project is licensed under the MIT License.
