import copy
import json
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


class QStore:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        if key in self.data:
            return self.data[key]
        return None


class StateStore:
    def __init__(self, path):
        self.path = path
        try:
            self.file = open(path, "r")
        except Exception as e:
            open(path, 'w').close()
            self.file = open(path, "r")
            logging.error(e)
        try:
            self.state = json.load(self.file)
        except Exception as e:
            self.state = {
                "version": "1.0",
                "services": []
            }
            self.flush()
            logging.error(e)

    def get_config(self):
        return copy.deepcopy(self.state)

    def set_services(self, services):
        self.state["services"] = []
        for service in services:
            self.state["services"].append(
                {
                    "url": service["url"],
                    "http_method": service["http_method"],
                    "violations": []
                }
            )
        self.flush()

    def add_violation(self, index: int, violation: str):
        state_changed = False
        if violation not in self.state["services"][index]["violations"]:
            self.state["services"][index]["violations"].append(violation)
            state_changed = True
        self.flush()
        return state_changed

    def remove_violation(self, index: int, violation: str):
        state_changed = False
        if violation in self.state["services"][index]["violations"]:
            self.state["services"][index]["violations"].remove(violation)
            state_changed = True
        self.flush()
        return state_changed

    def flush(self):
        tmp = open(self.path, 'w')
        json.dump(self.state, tmp, indent=4)
        self.file.flush()
