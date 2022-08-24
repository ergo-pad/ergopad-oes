import deepdiff
import time

from requests import Response

from storage.store import QStore


# DEFAULT MATCHERS


def status_code(resp: Response, config):
    try:
        return resp.ok
    except:
        return False


def exact(resp: Response, config):
    try:
        expected = config["response"]
        current = resp.json()
        return len(deepdiff.DeepDiff(expected, current).keys()) == 0
    except:
        return False


def types(resp: Response, config):
    try:
        expected = config["response"]
        current = resp.json()
        if type(expected) == list:
            return (type(current) == list)

        for key in expected:
            if type(expected[key]) != type(current[key]):
                return False
        return True
    except:
        return False


# CUSTOM MATCHERS

store = QStore()


def price_chart_matcher(resp: Response, config):
    THRESHOLD = 1800
    try:
        timestamp = time.time()
        current = resp.json()
        last = store.get("price_chart_matcher")
        if not last:
            store.set(
                "price_chart_matcher",
                {
                    "timestamp": timestamp,
                    "data": current
                }
            )
            return True

        if (len(deepdiff.DeepDiff(last["data"], current).keys()) == 0) and (last["timestamp"] + THRESHOLD < timestamp):
            return False

        store.set(
            "price_chart_matcher",
            {
                "timestamp": timestamp,
                "data": current
            }
        )
        return True
    except:
        return False


matcher_map = {
    "status_code": status_code,
    "types": types,
    "exact": exact,
    "price_chart_matcher": price_chart_matcher
}
