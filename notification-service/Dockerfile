FROM python:3.9-slim

WORKDIR /app

RUN pip install fastapi uvicorn

COPY notification.py .

CMD ["uvicorn", "notification:app", "--host", "0.0.0.0", "--port", "8000"]