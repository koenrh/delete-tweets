FROM python:3.8.0-alpine@sha256:695dadeb38c49d28a738dce0ef4d0716c2443ffca8f3a89f5e8258a4f27d71a4
COPY . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python", "/app/deletetweets.py"]
