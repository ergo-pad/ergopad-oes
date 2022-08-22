import json
import copy


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
        except:
            # file not found
            open(path, 'w').close()
            self.file = open(path, "r")
        try:
            self.state = json.load(self.file)
        except:
            # empty file
            self.state = {
                "version": "1.0",
                "services": []
            }
            self.flush()

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
