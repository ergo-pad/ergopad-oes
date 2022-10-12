import requests

def ergopad_unstake(address: str):
    stake_boxes = requests.post(
        "https://api.ergopad.io/staking/staked/",
        json={
            "addresses": [address]
        },
        timeout=10
    ).json()["addresses"][address]["stakeBoxes"]
    box_id = stake_boxes[0]["boxId"]
    stake_amount = stake_boxes[0]["stakeAmount"]
    payload = {
        "address": address,
        "addresses": [address],
        "stakeBox": box_id,
        "amount": stake_amount,
        "txFormat": "eip-12",
        "utxos": []
    }
    resp = requests.post(
       "https://api.ergopad.io/staking/unstake/",
       json=payload,
       timeout=10
    )
    return resp.ok


def paideia_unstake(address: str):
    stake_boxes = requests.post(
        "https://api.ergopad.io/staking/paideia/staked/",
        json={
            "addresses": [address]
        },
        timeout=10
    ).json()["addresses"][address]["stakeBoxes"]
    box_id = stake_boxes[0]["boxId"]
    stake_amount = stake_boxes[0]["stakeAmount"]
    payload = {
        "address": address,
        "addresses": [address],
        "stakeBox": box_id,
        "amount": stake_amount,
        "txFormat": "eip-12",
        "utxos": []
    }
    resp = requests.post(
       "https://api.ergopad.io/staking/paideia/unstake/",
       json=payload,
       timeout=10
    )
    return resp.ok

def paideia_unstakestake(address: str):
    stake_boxes = requests.post(
        "https://api.ergopad.io/staking/staked/",
        json={
            "addresses": [address]
        },
        timeout=10
    ).json()["addresses"][address]["stakeBoxes"]
    box_id = stake_boxes[0]["boxId"]
    stake_amount = stake_boxes[0]["stakeAmount"]
    payload = {
        "address": address,
        "addresses": [address],
        "stakeBox": box_id,
        "amount": stake_amount,
        "txFormat": "eip-12",
        "utxos": []
    }
    resp = requests.post(
       "https://api.ergopad.io/staking/unstake/",
       json=payload,
       timeout=10
    )
    return resp.ok


def paideia_addstake(address: str):
    stake_boxes = requests.post(
        "https://api.ergopad.io/staking/paideia/staked/",
        json={
            "addresses": [address]
        },
        timeout=10
    ).json()["addresses"][address]["stakeBoxes"]
    box_id = stake_boxes[0]["boxId"]
    stake_amount = 10
    payload = {
        "address": address,
        "addresses": [address],
        "stakeBox": box_id,
        "amount": stake_amount,
        "txFormat": "eip-12",
        "utxos": []
    }
    resp = requests.post(
       "https://api.ergopad.io/staking/paideia/addstake/",
       json=payload,
       timeout=10
    )
    return resp.ok
