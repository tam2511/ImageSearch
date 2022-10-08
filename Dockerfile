FROM python:3.8

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src src

CMD uvicorn src.main:app --reload --host "0.0.0.0" --port 8080
