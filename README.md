# ckb-wallet-balance

A Prometheus exporter that exposes the CKB wallet balance as a metric via the Mercury RPC API.

## Environment Variables

| Variable      | Required | Description                             | Example                                      |
|---------------|----------|-----------------------------------------|----------------------------------------------|
| `mercury_rpc` | Yes      | Mercury RPC endpoint URL                | `http://mercury-testnet.ckbapp.dev`          |
| `ckb_wallet`  | Yes      | CKB wallet address to monitor           | `ckt1qyqf3xlyd4tr55sc95efgatcfgj6988s3yusmatxk4` |

## Endpoints

| Path               | Description                              |
|--------------------|------------------------------------------|
| `/metrics/balance` | Prometheus metrics with wallet balance   |
| `/health`          | Health check — returns `{"status":"ok"}` |

## Run in Docker

```bash
docker run -d -p 3000:3000 \
  -e mercury_rpc=http://mercury-testnet.ckbapp.dev \
  -e ckb_wallet=ckt1qyqf3xlyd4tr55sc95efgatcfgj6988s3yusmatxk4 \
  jiangxianliang/ckb-balance:latest
```

## Health Check

```bash
curl http://127.0.0.1:3000/health
# {"status": "ok"}
```

## Metrics

```bash
curl http://127.0.0.1:3000/metrics/balance
```

## Local Run

```bash
pip install -r requirements.txt
export mercury_rpc=http://mercury-testnet.ckbapp.dev
export ckb_wallet=ckt1qyqf3xlyd4tr55sc95efgatcfgj6988s3yusmatxk4
python3 ckb_balance.py
```
