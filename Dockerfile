FROM python:3.8.0-alpine@sha256:57535e5b812e0416be9f994bf44309d955b7e6edc075ec9909aedcce41282c31
COPY . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python", "/app/deletetweets.py"]
