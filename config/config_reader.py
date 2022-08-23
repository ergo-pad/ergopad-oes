import json
import copy

from processor.matchers import matcher_map


class ConfigReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path, "r")
        self.config = json.load(self.file)

    def get_config(self):
        return copy.deepcopy(self.config)

    @staticmethod
    def validate_service(service):
        assert(type(service["url"]) == str)
        assert(service["http_method"] in (
            "GET", "PATCH", "POST", "PUT", "DELETE"))
        assert(service["response_matcher"] in matcher_map)
        assert(type(service["latency"]) == int)
