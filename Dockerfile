FROM python:3.9

WORKDIR /config
COPY ./ckb_balance.py ./requirements.txt /config/
RUN pip3 install -r requirements.txt
ENV PORT=3000

CMD "python3" "ckb_balance.py" "$mercury_rpc" "$ckb_wallet"
