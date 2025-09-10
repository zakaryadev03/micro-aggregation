FROM python:3.11

WORKDIR /app

COPY amazon/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY amazon/src .

CMD ["python", "consumer.py"]