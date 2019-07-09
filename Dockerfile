FROM python:3.7.4-alpine@sha256:fabd15bc1b5c6f4097cabae02122250f51d6fda4ab4729d1ba17f01028a7fc15
COPY . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python", "/app/deletetweets.py"]
