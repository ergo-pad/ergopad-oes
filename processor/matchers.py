import deepdiff
import time

from requests import Response

from storage.store import QStore
from processor.utxo_executor import ergopad_unstake, paideia_unstake, paideia_addstake

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


def non_empty(resp: Response, config):
    try:
        if not resp.ok:
            return False
        data = resp.json()
        if type(data) == list:
            return len(data) > 0
        else:
            return len(data.keys()) > 0
    except:
        return False


# CUSTOM MATCHERS

store = QStore()


def price_chart_matcher(resp: Response, config):
    THRESHOLD = 1800
    try:
        if not resp.ok:
            return False
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


def utxo_executor(_, config):
    try:
        if config["payload"]["method"] == "ergopad_unstake":
            return ergopad_unstake(config["payload"]["address"])
        if config["payload"]["method"] == "paideia_unstake":
            return paideia_unstake(config["payload"]["address"])
        if config["payload"]["method"] == "paideia_addstake":
            return paideia_addstake(config["payload"]["address"])
        return True
    except:
        return False


matcher_map = {
    "status_code": status_code,
    "types": types,
    "exact": exact,
    "non_empty": non_empty,
    "price_chart_matcher": price_chart_matcher,
    "utxo_executor": utxo_executor
}
