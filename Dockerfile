FROM python:3.7.3-alpine@sha256:8ea1d32c356382e51d9983f7ba5fa7d29c1fb4c86855e2f51686660a22416476
COPY . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python", "/app/deletetweets.py"]
