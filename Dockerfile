FROM python:3.7.4-alpine@sha256:488bfa82d8ac22f1ed9f1d4297613a920bf14913adb98a652af7dbbbf1c3cab9
COPY . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python", "/app/deletetweets.py"]
