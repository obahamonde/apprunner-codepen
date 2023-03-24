FROM python:3.8.2-slim-buster

ARG LOCAL_PATH

WORKDIR /app

COPY ${LOCAL_PATH}/requirements.txt /app

RUN pip install --upgrade pip \    
    pip install --no-cache-dir -r requirements.txt

COPY ${LOCAL_PATH} /app

CMD ["python", "main.py"]