import json
import copy

class ConfigReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path, "r")
        self.config = json.load(self.file)

    def get_config(self):
        return copy.deepcopy(self.config)
