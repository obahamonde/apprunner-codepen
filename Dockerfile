FROM python:3.8.2-slim-buster

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip \    
    pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "main.py"]