import os
import schedule
import time
import asyncio
from telegram import Bot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

messages = [
    "Good Morning! Aaj ka din accha ho",
    "Dopahar reminder: Paani piyo",
    "Shaam reminder: Rest karo",
]

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
while True:
    schedule.run_pending()
    time.sleep(60)
