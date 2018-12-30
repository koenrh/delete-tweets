FROM python:3.7.2-alpine@sha256:f708ad35a86f079e860ecdd05e1da7844fd877b58238e7a9a588b2ca3b1534d8
COPY . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python", "/app/deletetweets.py"]
