FROM python:3.11-slim

WORKDIR /app

ENV TZ=UTC

RUN apt-get update && apt-get install -y cron tzdata

COPY . .

RUN pip install fastapi uvicorn pyotp cryptography

RUN mkdir /data /cron

EXPOSE 8080

CMD service cron start && uvicorn app:app --host 0.0.0.0 --port 8080
