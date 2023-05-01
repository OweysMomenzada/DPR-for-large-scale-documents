# PLEASE GET THE MODEL BEFORE RUNNING THIS FILE
FROM python:3.8.13-slim

RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt --no-cache-dir && \
    pip install --upgrade pip

RUN rm -f app.py
EXPOSE 8501

CMD ["streamlit", "run", "demo.py"]