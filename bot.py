import discord
from dotenv import load_dotenv
import datetime
import os
import requests
import json
import random

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is online!")

@client.event
async def on_message(message):
    now_time = datetime.datetime.now()
    now_time_formatted = now_time.strftime("%Y-%m-%d %H:%M")

    def start_record():
        if os.path.exists("record.json"):
            with open("record.json", "r") as file:
                data = json.load(file)
        else:
            data = {}

        data["main_user"] = {
            "start_time": now_time_formatted,
            "current_streak": 0,
            "top_streak": 0
        }

        with open("record.json", "w") as file:
            json.dump(data, file, indent=2)

    if message.author == client.user:
        return

    if message.content.startswith('!hi'):
        await message.channel.send("Hello!")

    if message.content.startswith('!gif'):
        giphy_key = os.getenv("GIPHY_KEY")
        url = "https://api.giphy.com/v1/gifs/random"
        params = {
            "api_key": giphy_key,
            "tag": "fist bump",  # leave blank for totally random
            "rating": "" 
        }

        response = requests.get(url, params=params)
        data = response.json()

        gif_url = data["data"]["images"]["original"]["url"]

        await message.channel.send(gif_url)

    if message.content.startswith('!since'):
        time_string = message.content[7:]
        past_time = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M")
        difference = now_time - past_time
        difference_hour = difference.total_seconds() / 3600
        await message.channel.send(f"It’s been {difference_hour:.0f} hours since that time.")

    if message.content.startswith('!start'):
        if not os.path.exists("record.json"):
            start_record()
            await message.channel.send("Tracking started! 💪")
        else:
            with open("record.json", "r") as file:
                data = json.load(file)

            if "main_user" in data and "start_time" in data["main_user"]:
                await message.channel.send("You already started! Use !end before starting again.")
            else:
                start_record()
                await message.channel.send("Tracking started! 💪")
    
    if message.content.startswith('!end'):
        if os.path.exists("record.json"):
            with open("record.json", "r") as file:
                data = json.load(file)
        else:
            await message.channel.send("You do a great job!")

client.run(os.getenv("DISCORD_TOKEN"))