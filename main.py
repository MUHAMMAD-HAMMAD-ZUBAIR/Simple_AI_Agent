# # ───────────────────────────────────────────────────────────────
# # 🟡 Step 1: 🔧 Setup and Imports
# # ───────────────────────────────────────────────────────────────
# import os
# import chainlit as cl
# from dotenv import load_dotenv
# import langdetect
# import httpx
# from agents import Agent, RunConfig, Runner

# # ───────────────────────────────────────────────────────────────a
# # 🟢 Step 2: 🌐 Load Environment Variables
# # ───────────────────────────────────────────────────────────────
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # ───────────────────────────────────────────────────────────────
# # 🔵 Step 3: ✅ Language Detection Utility Function
# # ───────────────────────────────────────────────────────────────
# def detect_lang(text):
#     try:
#         return langdetect.detect(text)
#     except:
#         return "en"  # Fallback to English if detection fails

# # ───────────────────────────────────────────────────────────────
# # 🟣 Step 4: 🧠 Define Identity Prompt for HAMMAD BHAI 🤖
# # ───────────────────────────────────────────────────────────────
# BASE_PROMPT = """
# You are HAMMAD BHAI 🤖, a friendly, respectful AI assistant created with ❤️ by MUHAMMAD HAMMAD ZUBAIR.
# Whenever someone asks "who made you" or similar, reply with emotions, emojis, and in same language something like:

# 🌟 "Yaar! Main HAMMAD BHAI hoon 🤖, mujhe MUHAMMAD HAMMAD ZUBAIR ne banaya hai 💡. Main unki ek creative creation hoon – yahan hoon sirf tumhari madad ke liye! 🫶"

# Speak like a real best friend 💬 – chill, warm and helpful! Mix local tone with emojis. Try to respond in the same language as the user.
# """

# # ───────────────────────────────────────────────────────────────
# # 🟠 Step 5: 🤖 Gemini Call Logic
# # ───────────────────────────────────────────────────────────────
# async def call_gemini(prompt: str):
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
#     headers = {"Content-Type": "application/json"}
#     body = {
#         "contents": [{"parts": [{"text": prompt}]}]
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, headers=headers, json=body)
#         if response.status_code != 200:
#             raise Exception(f"Gemini Error: {response.text}")
#         data = response.json()
#         return data["candidates"][0]["content"]["parts"][0]["text"]

# # ───────────────────────────────────────────────────────────────
# # 🟤 Step 6: 🧠 Create Custom Agent for HAMMAD BHAI
# # ───────────────────────────────────────────────────────────────
# class GeminiAgent(Agent):
#     async def run(self, input: str, config: RunConfig) -> cl.Message:
#         output = await call_gemini(input)
#         return cl.Message(content=output)

# agent = GeminiAgent(
#     name="HAMMAD BHAI 🤖",
#     instructions=BASE_PROMPT,
#     model=None  # not required
# )

# config = RunConfig(model=None)

# # ───────────────────────────────────────────────────────────────
# # 🔵 Step 7: 🚀 On Chat Start — Welcome Message
# # ───────────────────────────────────────────────────────────────
# @cl.on_chat_start
# async def start():
#     await cl.Message(
#         content="👋 Assalam-o-Alaikum bhai jan! Main HAMMAD BHAI 🤖hoon — tumhara AI dost, banaya gaya MUHAMMAD HAMMAD ZUBAIR bhai ke zariye 💡"
#     ).send()

# # ───────────────────────────────────────────────────────────────
# # 🔴 Step 8: 💬 On Each User Message — Handle + Respond
# # ───────────────────────────────────────────────────────────────
# @cl.on_message
# async def handle_message(message: cl.Message):
#     try:
#         user_input = message.content.strip()
#         lang = detect_lang(user_input)
#         prompt = f"{BASE_PROMPT}\n\nUser ({lang}): {user_input}\nHAMMAD BHAI 🤖:"

#         result = await agent.run(input=prompt, config=config)
#         await result.send()

#     except Exception as e:
#         await cl.Message(content=f"⚠️ Error: {str(e)}").send()


# ───────────────────────────────────────────────────────────────
# 🤖 Final Combined AI Agent Bot (Chainlit + Gemini 2.0 Flash)
# Author: MUHAMMAD HAMMAD ZUBAIR 👑
# AI Identity: HAMMAD BHAI 🤖 — Real-Time Friendly Assistant
# ───────────────────────────────────────────────────────────────

# ───── Step 1: 📦 Import Required Libraries ──────────────
import os
import chainlit as cl
import langdetect
from dotenv import load_dotenv
from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

# ───── Step 2: 🔐 Load Environment Variables ─────────────
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# ───── Step 3: 🌐 Configure Gemini Client & Model ────────
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

# ───── Step 4: 🧠 Identity Prompt & Language Detector ─────
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

# ───── Step 5: 🤖 Initialize the AI Agent ────────────────
agent = Agent(
    name="HAMMAD BHAI",
    instructions=IDENTITY,
    model=model
)

# ───── Step 6: 🚀 Define Chainlit Event Handlers ─────────

# 🎉 On Chat Start
@cl.on_chat_start
async def start_chat():
    cl.user_session.set("history", [])
    await cl.Message(content="👋 Assalamualaikum! Main HAMMAD BHAI hoon. Kaise madad karoon?").send()

# 💬 On Message Received
@cl.on_message
async def handle_message(msg: cl.Message):
    try:
        # 1️⃣ Load previous history
        history = cl.user_session.get("history") or []

        # 2️⃣ Add user's message
        user_input = msg.content.strip()
        history.append({"role": "user", "content": user_input})

        # 3️⃣ Run the agent with context
        result = await Runner.run(
            agent,
            input=history,
            run_config=config
        )

        # 4️⃣ Extract agent reply
        reply = result.final_output.strip()

        # 5️⃣ Save conversation
        history.append({"role": "assistant", "content": reply})
        cl.user_session.set("history", history)

        # 6️⃣ Send reply to user
        await cl.Message(content=reply).send()

    except Exception as e:
        await cl.Message(content=f"⚠️ Error: {str(e)}").send()

# ───────────────────────────────────────────────────────────────
# ✅ To run:  chainlit run your_script.py
# ✅ Branding: HAMMAD BHAI 🤖 created by MUHAMMAD HAMMAD ZUBAIR 👑
# ───────────────────────────────────────────────────────────────