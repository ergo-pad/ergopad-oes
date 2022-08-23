from storage.store import QStore


class StatsEngine:
    MOVING_AVG = 7

    def __init__(self, services):
        self.store = QStore()
        for service in services:
            self.store.set(
                (service["url"], service["http_method"], "error"), []
            )
            self.store.set(
                (service["url"], service["http_method"], "latency"), []
            )

    def add_error_data_point(self, url: str, http_method: str, value: int):
        assert(value == 0 or value == 1)
        if len(self.store.get((url, http_method, "error"))) == StatsEngine.MOVING_AVG:
            self.store.get((url, http_method, "error")).pop(0)
        self.store.get((url, http_method, "error")).append(value)

    def add_latency_data_point(self, url: str, http_method: str, value: int):
        if len(self.store.get((url, http_method, "latency"))) == StatsEngine.MOVING_AVG:
            self.store.get((url, http_method, "latency")).pop(0)
        self.store.get((url, http_method, "latency")).append(value)

    def get_error_rate(self, url: str, http_method: str):
        if len(self.store.get((url, http_method, "error"))) < StatsEngine.MOVING_AVG:
            return 0
        return sum(self.store.get((url, http_method, "error"))) / \
            StatsEngine.MOVING_AVG

    def get_avg_latency(self, url: str, http_method: str):
        if len(self.store.get((url, http_method, "latency"))) < StatsEngine.MOVING_AVG:
            return 0
        return sum(self.store.get((url, http_method, "latency"))) / \
            StatsEngine.MOVING_AVG
