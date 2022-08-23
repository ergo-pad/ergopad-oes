import os

from config.config_reader import ConfigReader
from storage.store import StateStore
from processor.stats import StatsEngine


def test_always_passes():
    return True


def test_config_reader():
    config_reader = ConfigReader(os.getenv("CONFIG_PATH"))

    assert(config_reader.get_config()["version"] == "1.0")
    assert(type(config_reader.get_config()["cool_down"]) == int)
    assert(
        0 < config_reader.get_config()["error_threshold"] and
        config_reader.get_config()["error_threshold"] <= 1
    )
    assert(type(config_reader.get_config()["services"]) == list)
    for service in config_reader.get_config()["services"]:
        ConfigReader.validate_service(service)


def test_state_store():
    state_store = StateStore(os.getenv("STATE_PERSISTENCE_PATH"))
    state_store.set_services(
        [
            {
                "url": "https://test.com",
                "http_method": "GET"
            }
        ]
    )
    assert(state_store.get_config()["services"]
           [0]["url"] == "https://test.com")
    assert(state_store.get_config()["services"][0]["http_method"] == "GET")
    state_store.add_violation(0, "latency")
    assert("latency" in state_store.get_config()["services"][0]["violations"])
    state_store.add_violation(0, "error")
    assert("error" in state_store.get_config()["services"][0]["violations"])
    state_store.remove_violation(0, "latency")
    assert(
        "latency" not in state_store.get_config()["services"][0]["violations"]
    )


def test_stats():
    url = "https://test.com"
    http_method = "GET"
    stats_m = StatsEngine([
        {
            "url": url,
            "http_method": http_method
        }
    ])
    stats_m.add_error_data_point(url, http_method, 0)
    stats_m.add_error_data_point(url, http_method, 0)
    stats_m.add_error_data_point(url, http_method, 0)
    stats_m.add_error_data_point(url, http_method, 0)
    stats_m.add_error_data_point(url, http_method, 0)
    stats_m.add_error_data_point(url, http_method, 0)
    stats_m.add_error_data_point(url, http_method, 1)
    stats_m.add_error_data_point(url, http_method, 1)
    assert(stats_m.get_error_rate(url, http_method) == (2 / 7))
    stats_m.add_error_data_point(url, http_method, 1)
    assert(stats_m.get_error_rate(url, http_method) == (3 / 7))
    stats_m.add_latency_data_point(url, http_method, 100)
    stats_m.add_latency_data_point(url, http_method, 200)
    stats_m.add_latency_data_point(url, http_method, 300)
    stats_m.add_latency_data_point(url, http_method, 400)
    stats_m.add_latency_data_point(url, http_method, 500)
    stats_m.add_latency_data_point(url, http_method, 600)
    stats_m.add_latency_data_point(url, http_method, 700)
    assert(stats_m.get_avg_latency(url, http_method) == (2800 / 7))
    stats_m.add_latency_data_point(url, http_method, 800)
    assert(stats_m.get_avg_latency(url, http_method) == (3500 / 7))
