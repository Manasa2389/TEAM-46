from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai

# --- CONFIGURATION ---
# 1. Get the API Key (Uses the key you provided)
# We check the environment variable first, but fallback to your specific key.
API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash"

# 2. Configure the Gemini Library
if not API_KEY:
    print("CRITICAL ERROR: API_KEY is missing.")
else:
    genai.configure(api_key=API_KEY)


# --- FastAPI App Setup ---
app = FastAPI(title="Voice-to-Voice Gemini Assistant")

# 3. Enable CORS (Critical for connecting to index.html)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows your local HTML file to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Model ---
class ChatRequest(BaseModel):
    prompt: str

# --- API Endpoint ---
@app.post("/chat")
def chat_endpoint(data: ChatRequest):
    """
    Receives text from the frontend, sends it to Gemini, and returns the response.
    """
    user_input = data.prompt.strip()
    
    try:
        # Initialize the model
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Start a chat session (or just generate content)
        # Using start_chat allows for a conversational context if needed, 
        # but here we treat it as a single turn for simplicity.
        chat = model.start_chat(history=[])
        
        # Send message to Gemini
        # We disable streaming here to send the full text back to the frontend at once
        response = chat.send_message(user_input, stream=False)
        
        # Extract text
        ai_text = response.text
        
        return {"response": ai_text}

    except Exception as e:
        print(f"Gemini Error: {e}")
        return {"response": "I'm sorry, I'm having trouble connecting to my brain right now. Please try again."}

# --- Health Check ---
@app.get("/")
def home():
    return {"status": "Gemini Voice Assistant is Running"}
