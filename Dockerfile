FROM python:3.11

WORKDIR /app/

COPY requirements.txt entrypoint.sh /

RUN pip install -r /requirements.txt

COPY src ./
