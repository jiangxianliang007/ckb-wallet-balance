FROM python:3.11-slim

WORKDIR /config

COPY requirements.txt /config/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ckb_balance.py /config/

RUN useradd --no-create-home --shell /bin/false appuser
USER appuser

EXPOSE 3000

ENV PORT=3000

CMD ["python3", "ckb_balance.py"]
