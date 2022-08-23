import discord
import dotenv
import os
import queue

from discord.ext import tasks

dotenv.load_dotenv()

channel_filter = (int(os.getenv("DISCORD_CHANNEL_ID")),)
client = discord.Client(intents=discord.Intents.default())

message_q = queue.Queue()


@tasks.loop(seconds=30)
async def handler():
    while not message_q.empty():
        message = message_q.get()
        for channel in client.get_all_channels():
            if channel.id not in channel_filter:
                continue
            try:
                await channel.send(message)
            except:
                pass


@client.event
async def on_ready():
    handler.start()


# @client.event
# async def on_message(message: discord.Message):
#     print(message.channel.id)


class DiscordBot:
    def __init__(self):
        self.client = client

    def send_message(self, service: dict, event: str):
        event_text = event
        if event == "error":
            event_text = "error rates"
        message = f"""```
----------------
New Issue Found:
----------------
Service: [{service["http_method"]}] {service["url"]} is experiencing high {event_text}

[Operational Excellence Services]
```
"""
        message_q.put(message)

    def start(self):
        client.run(os.getenv("DISCORD_BOT_TOKEN"))
