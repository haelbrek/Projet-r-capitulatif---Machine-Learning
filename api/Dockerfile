
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app
RUN     pip install -r requirements.txt

    # pip install joblib && \
    # pip install -U scikit-learn && \
    # pip install xgboost && \

COPY . /app

CMD ["uvicorn", "main:app",  "--host", "0.0.0.0", "--port", "8000"]
