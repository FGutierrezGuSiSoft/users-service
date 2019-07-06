FROM python:3.7.3-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./src /usr/src/app

CMD ["flask", "run", "--host=0.0.0.0"]
