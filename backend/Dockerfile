FROM python:3.13-slim

WORKDIR /app

RUN groupadd --system appgroup \
    && useradd --system \
       --gid appgroup \
       --home-dir /app \
       appuser

COPY requirements.txt .

RUN pip install --no-cache-dir \
    -r requirements.txt

COPY app ./app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
