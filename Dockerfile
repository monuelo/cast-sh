FROM python:3.6
MAINTAINER Héricles "hericles.me@gmail.com"

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python", "-m", "cast"]
