# ckb-wallet-balance

run in docker
```
docker run -d -it -p 3200:3000 -e mercury_rpc=http://mercury-testnet.ckbapp.dev -e ckb_wallet=ckt1qyqf3xlyd4tr55sc95efgatcfgj6988s3yusmatxk4 jiangxianliang/ckb-balance:0.1

curl http://127.0.0.1:3000/metrics/balance
```
