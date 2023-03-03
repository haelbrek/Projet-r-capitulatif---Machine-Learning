
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY . /app

RUN pip install --upgrade pip && \
    pip install joblib && \
    pip install requests && \
    pip install -r requirements.txt

EXPOSE 8001



CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]

