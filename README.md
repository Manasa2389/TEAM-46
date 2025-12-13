# 🧠 Mental Health Voice Chatbot (Voice-to-Voice Copilot)

A **real-time voice-enabled mental health chatbot** built using **FastAPI**, **OpenAI GPT**, **Speech Recognition**, and **Text-to-Speech (gTTS)**.
Users can **speak** to the chatbot 🎤 and receive **spoken responses** 🔊, making it interactive, accessible, and user-friendly.

---

## 🚀 Project Overview

Mental health support is often limited by accessibility and stigma. This project aims to provide a **supportive conversational AI assistant** that allows users to communicate **hands-free using voice**, helping them express thoughts more naturally.

⚠️ **Disclaimer:** This chatbot is for **support purposes only** and is **not a replacement for professional mental health care**.

---

## ✨ Features

* 🎙️ **Speech-to-Text (STT)** using browser speech recognition
* 🤖 **AI-powered responses** using OpenAI GPT
* 🔊 **Text-to-Speech (TTS)** using gTTS
* 🔁 **Session-based conversations** (context preserved)
* 🌐 **Single-file full-stack app** (frontend + backend combined)
* ⚡ **FastAPI backend** for high performance
* 🧩 Easy to run in **VS Code**

---

## 🛠️ Technologies Used

### Backend

* **Python 3.10+**
* **FastAPI** – backend framework
* **OpenAI API** – conversational AI
* **gTTS (Google Text-to-Speech)** – voice output
* **Uvicorn** – ASGI server

### Frontend

* **HTML5**
* **JavaScript**
* **Web Speech API** – voice input (SpeechRecognition)
* **CSS** – simple UI styling

---

## 📂 Project Structure

```
mental_health_chatbot/
│
├── main.py        # Combined frontend + backend code
├── README.md      # Project documentation
```

---

## ⚙️ Setup Instructions (Run in VS Code)

### 1️⃣ Clone or Create Project Folder

```bash
mkdir mental_health_chatbot
cd mental_health_chatbot
```

Create a file named **`main.py`** and paste the combined code into it.

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install fastapi uvicorn openai gtts
```

---

### 4️⃣ Set OpenAI API Key

⚠️ **Do NOT hardcode your API key in the source code**

**Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY="your_openai_api_key"
```

**macOS / Linux:**

```bash
export OPENAI_API_KEY="your_openai_api_key"
```

---

### 5️⃣ Run the Application

```bash
uvicorn main:app --reload
```

You should see:

```
Uvicorn running on http://127.0.0.1:8000
```

---

### 6️⃣ Open in Browser 🌐

Visit:

```
http://127.0.0.1:8000
```

Click **🎤 Speak**, talk to the chatbot, and listen to the AI response!

---

## 🔄 How It Works

1. 🎙️ User speaks using the browser microphone
2. 📝 Speech is converted to text (SpeechRecognition API)
3. 📡 Text is sent to FastAPI `/chat` endpoint
4. 🤖 OpenAI GPT generates a response
5. 🔊 Response is converted to speech using gTTS
6. 📢 Audio is sent back and played in the browser

---

## 🧠 Use Cases

* Mental health support companion
* Stress relief conversations
* Voice-based AI assistant demo
* Hackathon-ready AI project
* Accessibility-focused chatbot

---

## 🔐 Security Notes

* ❌ Never expose your OpenAI API key in public repositories
* ✅ Use environment variables for secrets
* ⚠️ This app stores conversations **in-memory only** (not persistent)

---

## 🚧 Future Enhancements

* 💬 Chat bubble UI (user vs bot)
* 🌈 Improved UI with Tailwind / CSS animations
* 🧠 Sentiment analysis for emotional awareness
* 🗂️ Database-backed conversation history
* 🌍 Multi-language voice support

---

## 🏁 Conclusion

This project demonstrates how **voice, AI, and web technologies** can be combined to create an **interactive mental health copilot**. It is lightweight, hackathon-friendly, and easy to extend.

💡 *Built with passion for accessible AI solutions.*

---

### 🙌 Happy Coding & Take Care of Your Mental Health 💙
