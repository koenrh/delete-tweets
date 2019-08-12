FROM python:3.7.4-alpine@sha256:e9ba2f4a76724915342df7908f6bc529d3d6c7cd98cde752c5ae569d0741e9fc
COPY . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python", "/app/deletetweets.py"]
