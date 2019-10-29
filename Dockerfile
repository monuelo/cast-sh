FROM ubuntu:latest

MAINTAINER Héricles "hericles.me@gmail.com"

RUN apt-get update
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv

COPY ../cast-bak /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "cast"]