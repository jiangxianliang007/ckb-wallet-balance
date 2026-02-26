# encoding: utf-8

import json
import logging
import os

import prometheus_client
import requests
from flask import Flask, Response, jsonify
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

MERCURY_RPC = os.environ.get("mercury_rpc")
CKB_WALLET = os.environ.get("ckb_wallet")

if not MERCURY_RPC:
    raise RuntimeError("Environment variable 'mercury_rpc' is not set.")
if not CKB_WALLET:
    raise RuntimeError("Environment variable 'ckb_wallet' is not set.")

app = Flask(__name__)

CKB_CHAIN_REGISTRY = CollectorRegistry(auto_describe=False)
WALLET_BALANCE_GAUGE = Gauge(
    "get_wallet_balance",
    "Get wallet_balance, Show ckb wallet balance",
    ["ckb_wallet"],
    registry=CKB_CHAIN_REGISTRY,
)


BALANCE_ERROR_VALUE = -1


def convert_int(value):
    """Convert a decimal or hexadecimal string to an integer.

    Args:
        value: A string representing a decimal or hexadecimal integer.

    Returns:
        The integer value.

    Raises:
        ValueError: If the value cannot be converted from decimal or hex.
        TypeError: If the value is not a string or integer type.
    """
    try:
        return int(value)
    except ValueError:
        return int(value, base=16)


class MercuryRpcClient:
    def __init__(self, mercury_rpc):
        self.mercury_rpc = mercury_rpc

    def get_mercury_info(self):
        headers = {"Content-Type": "application/json"}
        payload = {
            "id": 42,
            "jsonrpc": "2.0",
            "method": "get_balance",
            "params": [
                {
                    "item": {"type": "Address", "value": CKB_WALLET},
                    "asset_infos": [],
                    "tip_block_number": None,
                }
            ],
        }
        try:
            r = requests.post(
                url=self.mercury_rpc,
                data=json.dumps(payload),
                headers=headers,
                timeout=30,
            )
            balance_entry = r.json()["result"]["balances"][0]
            return {
                "wallet_balance": convert_int(balance_entry["free"]) // 100000000,
            }
        except requests.RequestException as exc:
            logger.error("Request to Mercury RPC failed: %s", exc)
            return {"wallet_balance": BALANCE_ERROR_VALUE}
        except (KeyError, IndexError, ValueError) as exc:
            logger.error("Unexpected response format from Mercury RPC: %s", exc)
            return {"wallet_balance": BALANCE_ERROR_VALUE}


@app.route("/metrics/balance")
def rpc_get():
    client = MercuryRpcClient(MERCURY_RPC)
    info = client.get_mercury_info()
    WALLET_BALANCE_GAUGE.labels(ckb_wallet=CKB_WALLET).set(info["wallet_balance"])
    return Response(prometheus_client.generate_latest(CKB_CHAIN_REGISTRY), mimetype="text/plain")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    logger.info("Starting ckb-wallet-balance: mercury_rpc=%s, ckb_wallet=%s", MERCURY_RPC, CKB_WALLET)
    app.run(host="0.0.0.0", port=3000, debug=False)
