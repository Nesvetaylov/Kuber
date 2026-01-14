FROM python:3.9-slim

WORKDIR /app

RUN pip install fastapi uvicorn

COPY profile.py .

CMD ["uvicorn", "profile:app", "--host", "0.0.0.0", "--port", "8000"]