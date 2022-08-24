import logging
import requests
import threading
import time

from notifications.discord.bot import DiscordBot
from processor.matchers import matcher_map
from processor.stats import StatsEngine
from storage.store import StateStore

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


class OpsProcessor:
    BUFFER = 2

    def __init__(self, config: dict, state_store: StateStore, notification_service: DiscordBot):
        self.config = config
        self.stats = StatsEngine(config["services"])
        self.state = state_store
        self.notification_service = notification_service

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        cool_down = self.config["cool_down"]
        error_threshold = self.config["error_threshold"]
        services = self.config["services"]
        while True:
            for index, service in enumerate(services):
                url = service["url"]
                http_method = service["http_method"]
                matcher = matcher_map[service["response_matcher"]]
                latency = service["latency"]
                try:
                    start_time = time.time()
                    res = requests.request(
                        http_method,
                        url=url,
                        data=service["payload"] if "payload" in service else None,
                        timeout=5,
                    )
                    end_time = time.time()

                    error = (not matcher(res, service))
                    current_latency = int((end_time - start_time) * 1000)
                    self.stats.add_error_data_point(url, http_method, error)
                    self.stats.add_latency_data_point(
                        url, http_method, current_latency
                    )
                except Exception as e:
                    self.stats.add_error_data_point(url, http_method, 1)
                    logging.error(e)

                error_rate = self.stats.get_error_rate(url, http_method)
                avg_latency = self.stats.get_avg_latency(url, http_method)
                self.handle_metrics(
                    index, error_rate, error_threshold, avg_latency, latency
                )

                time.sleep(OpsProcessor.BUFFER)

            time.sleep(cool_down)

    def handle_metrics(self, index, error_rate, error_threshold, avg_latency, latency_threshold):
        logging.info(f'service #{index} error_rate: {error_rate}')
        logging.info(f'service #{index} avg_latency: {avg_latency}')
        if error_rate > error_threshold:
            if self.state.add_violation(index, "error"):
                self.notification_hook(self.config["services"][index], "error")
        else:
            self.state.remove_violation(index, "error")
        if avg_latency > latency_threshold:
            if self.state.add_violation(index, "latency"):
                self.notification_hook(
                    self.config["services"][index], "latency"
                )
        else:
            self.state.remove_violation(index, "latency")

    def notification_hook(self, service: dict, event: str):
        self.notification_service.send_message(service, event)
