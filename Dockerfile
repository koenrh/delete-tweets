FROM python:2.7-alpine@sha256:cbc1c1c227012034793083306f6f6322e0276ca134c218cc49b131ca59df7699
COPY . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python", "/app/deletetweets.py"]
