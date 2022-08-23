import dotenv
import os

from config.config_reader import ConfigReader
from notifications.discord.bot import DiscordBot
from processor.core import OpsProcessor
from storage.store import StateStore

dotenv.load_dotenv()


def main():
    config = ConfigReader(os.getenv("CONFIG_PATH")).get_config()
    state_store = StateStore(os.getenv("STATE_PERSISTENCE_PATH"))
    state_store.set_services(config["services"])
    bot = DiscordBot()
    processor = OpsProcessor(config, state_store, bot)

    processor.start()
    bot.start()


# entry point
if __name__ == "__main__":
    main()
