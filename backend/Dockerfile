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
COPY tests ./tests
COPY pytest.ini ./pytest.ini

USER appuser

EXPOSE 8000

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#enable this line to disable access logs for cleaner output in production environments
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]