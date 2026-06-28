import os
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "schedule", "python-telegram-bot"])

import schedule
import time
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GROQ_KEY = os.environ.get("GROQ_KEY")

messages = [
    "Good Morning! Aaj ka din achha ho",
    "Dopahar reminder: Paani piyo",
    "Shaam reminder: Rest karo",
]

def ai_reply(user_message):
    if not GROQ_KEY:
        return "AI abhi available nahi hai"
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": "Bearer " + GROQ_KEY,
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
    )
    return response.json()['choices'][0]['message']['content']

async def send_message(text):
    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=text)
        print(f"Bheja: {text}")
    except Exception as e:
        print(f"Error: {e}")

def job1():
    asyncio.run(send_message(messages[0]))

def job2():
    asyncio.run(send_message(messages[1]))

def job3():
    asyncio.run(send_message(messages[2]))

schedule.every().day.at("08:00").do(job1)
schedule.every().day.at("14:00").do(job2)
schedule.every().day.at("19:00").do(job3)

print("Bot chalu hai!")
ai_msg = ai_reply("Ek chota motivational quote Hindi mein do")
asyncio.run(send_message("AI ka sandesh: " + ai_msg))

while True:
    schedule.run_pending()
    time.sleep(60)
