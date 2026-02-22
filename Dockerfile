
FROM python:3.12-slim AS builder

WORKDIR /app


RUN apt-get update && apt-get install -y build-essential


COPY requirements.txt .


RUN pip install --upgrade pip
RUN pip install --prefix=/install -r requirements.txt



FROM python:3.12-slim

WORKDIR /app


COPY --from=builder /install /usr/local


COPY . .

EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]