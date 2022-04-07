#encoding: utf-8

import requests
import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask, request, current_app
import os
import sys


Mercury_RPC = sys.argv[1]
CKB_wallet = sys.argv[2]

NodeFlask = Flask(__name__)

def convert_int(value):
    try:
        return int(value)
    except ValueError:
        return int(value, base=16)
    except Exception as exp:
        raise exp

class RpcGet(object):
    def __init__(self, Mercury_RPC):
        self.Mercury_RPC = Mercury_RPC

    def get_mercury_info(self):
        headers = {"Content-Type":"application/json"}
        data = '{"id": 42,"jsonrpc": "2.0","method": "get_balance","params": [ {"item": {"type": "Address","value": "%s"},"asset_infos": [],"tip_block_number": null}]}' % (CKB_wallet)
        try:
            r = requests.post(
                url="%s" %(self.Mercury_RPC),
                data=data,
                headers=headers
            )
            replay = r.json()["result"]["balances"][0]
            return {
                "wallet_balance": convert_int(replay["free"])//100000000,
            }
        except:
            return {
                "wallet_balance": "-1",
            }

@NodeFlask.route("/metrics/balance")
def rpc_get():
    CKB_Chain = CollectorRegistry(auto_describe=False)
    Get_Mercury_Info = Gauge("get_wallet_balance",
                                   "Get wallet_balance, Show ckb wallet balance",
                                   ["ckb_wallet"],
                                   registry=CKB_Chain)

    get_result = RpcGet(Mercury_RPC)
    mercury_last_block_info = get_result.get_mercury_info()
    Get_Mercury_Info.labels(
        ckb_wallet=CKB_wallet
    ).set(mercury_last_block_info["wallet_balance"])
    return Response(prometheus_client.generate_latest(CKB_Chain), mimetype="text/plain")

if __name__ == "__main__":
    NodeFlask.run(host="0.0.0.0",port=3000)
