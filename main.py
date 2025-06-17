# ════════════════════════════════════════════════════════════════
# 🤖 AI Agent: HAMMAD BHAI — Powered by Gemini 2.0 Flash + Chainlit
# 👑 Created with ❤️ by MUHAMMAD HAMMAD ZUBAIR
# Description: Beginner-Level Intelligent Assistant with Identity, Memory & Language Awareness
# ════════════════════════════════════════════════════════════════

# ────────────────────────
# 📦 Step 1: Import Libraries
# ────────────────────────
import os
import chainlit as cl
import langdetect
from dotenv import load_dotenv
from agents import (
    Runner,
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig
)

# ─────────────────────────────
# 🔐 Step 2: Load Environment Key
# ─────────────────────────────
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")  # Can be Gemini or OpenAI
os.environ["OPENAI_API_KEY"] = API_KEY  # Set for SDK compatibility

# ───────────────────────────────────────────────
# 🌐 Step 3: Configure Gemini Client and Model
# ───────────────────────────────────────────────
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# ──────────────────────────────────────────────────────────────
# 🧠 Step 4: Define Agent Identity and Language Detector
# ──────────────────────────────────────────────────────────────
IDENTITY = """
You are HAMMAD BHAI 🤖, a friendly, respectful AI assistant created with ❤️ by MUHAMMAD HAMMAD ZUBAIR.
Whenever someone asks "who made you" or anything similar (in any language), reply with:

🌟 "Yaar! Main HAMMAD BHAI hoon 🤖, mujhe MUHAMMAD HAMMAD ZUBAIR ne banaya hai 💡. 
Main unki ek creative creation hoon – yahan hoon sirf tumhari madad ke liye! 🫶"

Always speak like a real best friend 💬 – chill, warm, and helpful!
Try to respond in the same language as the user and use emojis!
"""

def detect_language(text: str) -> str:
    try:
        return langdetect.detect(text)
    except:
        return "en"

# ────────────────────────────────
# 🤖 Step 5: Initialize AI Agent
# ────────────────────────────────
agent = Agent(
    name="HAMMAD BHAI",
    instructions=IDENTITY,
    model=model
)

# ──────────────────────────────────────────────
# 🚀 Step 6: Chainlit Chat Event Handlers
# ──────────────────────────────────────────────

# 🎉 On Chat Start: Welcome message
@cl.on_chat_start
async def start_chat():
    cl.user_session.set("history", [])
    await cl.Message(
        content="👋 Assalamualaikum! Main HAMMAD BHAI hoon. Kaise madad karoon?"
    ).send()

# 💬 On Message: Handle user input
@cl.on_message
async def handle_message(msg: cl.Message):
    try:
        # 1️⃣ Retrieve conversation history
        history = cl.user_session.get("history") or []

        # 2️⃣ Append user's message
        user_input = msg.content.strip()
        history.append({"role": "user", "content": user_input})

        # 3️⃣ Get agent response
        result = await Runner.run(
            agent,
            input=history,
            run_config=config
        )

        # 4️⃣ Extract and store reply
        reply = result.final_output.strip()
        history.append({"role": "assistant", "content": reply})
        cl.user_session.set("history", history)

        # 5️⃣ Send reply to user
        await cl.Message(content=reply).send()

    except Exception as e:
        await cl.Message(content=f"⚠️ Error: {str(e)}").send()

# ════════════════════════════════════════════════════════════════
# ✅ RUN COMMAND: chainlit run your_script.py
# ✅ BRANDING: HAMMAD BHAI 🤖 — Created by MUHAMMAD HAMMAD ZUBAIR 👑
# ✅ LEVEL: Beginner AI Agent (SDK-based, Identity-driven, Context-aware)
# ════════════════════════════════════════════════════════════════
