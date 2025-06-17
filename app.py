# ───────────────────────────────────────────────────────────────
# 🤖 Combined AI Chatbot Code: Chainlit + Gemini 2.0 Flash (Polished)
# Author: MUHAMMAD HAMMAD ZUBAIR 👑
# Agent Identity: HAMMAD BHAI 🤖 — Created for Real-Time Assistance
# ───────────────────────────────────────────────────────────────

# 🔹 Step 1: 📦 Import Required Libraries
import os
import chainlit as cl
from dotenv import load_dotenv
import langdetect
import google.generativeai as genai

# 🔹 Step 2: 🌐 Load Environment Variables from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")  # Gemini API Key from .env file

# 🔹 Step 3: 🔐 Configure Gemini Client
# This prepares Gemini to work with your API key and settings
genai.configure(api_key=GOOGLE_API_KEY)

# 🔹 Step 4: 🧠 Setup Gemini Model with Generation Configs
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": 0.9,          # Creativity level
        "top_p": 1,                  # Diversity control
        "top_k": 40,                 # Token filtering
        "max_output_tokens": 2048,  # Max response size
    }
)

# 🔹 Step 5: 📛 Identity Prompt for HAMMAD BHAI 🤖
BASE_PROMPT = """
You are HAMMAD BHAI 🤖, a friendly, respectful AI assistant created with ❤️ by MUHAMMAD HAMMAD ZUBAIR.
Whenever someone asks "who made you" or anything similar (in any language), reply with emotions, emojis, and in the same language something like:

🌟 "Yaar! Main HAMMAD BHAI hoon 🤖, mujhe MUHAMMAD HAMMAD ZUBAIR ne banaya hai 💡. Main unki ek creative creation hoon – yahan hoon sirf tumhari madad ke liye! 🫶"

Speak like a real best friend 💬 – chill, warm and helpful! Mix local tone with emojis. Try to respond in the same language as the user.
"""

# 🔹 Step 6: 🌍 Language Detection Utility
# This helps respond in user's language
def detect_lang(text):
    try:
        return langdetect.detect(text)
    except:
        return "en"  # Default to English if detection fails

# 🔹 Step 8: 💬 Message Handler — Core Logic
@cl.on_message
async def handle_message(message: cl.Message):
    try:
        user_input = message.content.strip()
        lang = detect_lang(user_input)

        # 👇 Get or initialize chat history
        history = cl.user_session.get("history") or []

        # 👇 Add current user message to history
        history.append({"role": "user", "parts": [user_input]})

        # 👇 Create full context with identity as first message
        full_prompt = [{"role": "user", "parts": [BASE_PROMPT]}] + history

        # 👇 Get model response with full conversation context
        response = model.generate_content(full_prompt)

        # 👇 Add assistant response to history
        history.append({"role": "model", "parts": [response.text.strip()]})

        # 👇 Save updated history
        cl.user_session.set("history", history)

        # 👇 Send reply to frontend
        await cl.Message(content=response.text.strip()).send()

    except Exception as e:
        await cl.Message(content=f"⚠️ Error: {str(e)}").send()
