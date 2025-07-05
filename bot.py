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
    log_entry = {
        "author": message.author.name,
        "content": message.content,
        "timestamp": str(message.created_at)
    }

    def log_message():
        if os.path.exists("log.json"):
            with open("log.json", "r") as file:
                logs = json.load(file)
        else:
            logs = []

        logs.append(log_entry)
        
        with open("log.json", "w") as file:
            json.dump(logs, file, indent=2)
    
    #log_message()

    now_time = datetime.datetime.now()
    now_time_formatted = now_time.strftime("%Y-%m-%d %H:%M")

    if message.author == client.user:
        return

    if message.content.startswith('!hi'):
        await message.channel.send("Hello!")

    if message.content.startswith('!time'):
        await message.channel.send(str(now_time_formatted))

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

    if message.content.startswith("!quotes"):
        with open("quotes.json", "r") as file:
            data = json.load(file)
            quote = random.choice(data["quotes"])
            await message.channel.send(quote)


client.run(os.getenv("DISCORD_TOKEN"))