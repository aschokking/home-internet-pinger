FROM python:3.12-alpine

WORKDIR /code

COPY pinger/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "pinger/main.py"]