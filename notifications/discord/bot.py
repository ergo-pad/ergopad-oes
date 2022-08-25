import discord
import dotenv
import json
import logging
import os
import queue

from discord.ext import tasks

dotenv.load_dotenv()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

channel_filter = (int(os.getenv("DISCORD_CHANNEL_ID")),)
client = discord.Client(intents=discord.Intents.default())

message_q = queue.Queue()


@tasks.loop(seconds=30)
async def handler():
    logging.info("bot handler checking for new events")
    while not message_q.empty():
        message = message_q.get()
        for channel in client.get_all_channels():
            if channel.id not in channel_filter:
                continue
            try:
                await channel.send(message)
            except Exception as e:
                logging.error(e)


@tasks.loop(hours=24)
async def daily_reporter():
    logging.info("bot generating daily state report")
    try:
        fp = open("state.json", "r")
        state = json.load(fp)
        message = f"""```
------------------
Daily Issue Report
------------------

state.json
{json.dumps(state, indent=4)}

[Operational Excellence Services]
```
"""
        for channel in client.get_all_channels():
            if channel.id not in channel_filter:
                continue
            await channel.send(message)

    except Exception as e:
        logging.error(e)


@client.event
async def on_ready():
    try:
        handler.start()
    except Exception as e:
        logging.error(e)


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
