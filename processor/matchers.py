from requests import Response


def status_code(resp: Response, config):
    return resp.ok


matcher_map = {
    "status_code": status_code
}
