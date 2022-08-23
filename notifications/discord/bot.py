import discord
import dotenv
import os

dotenv.load_dotenv()
client = discord.Client(intents=discord.Intents.default())


class DiscordBot:
    def __init__(self):
        self.client = client

    def send_message(self, service: dict, event: str):
        print(service, event)

    def start(self):
        client.run(os.getenv("DISCORD_BOT_TOKEN"))
