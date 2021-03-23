FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y python3-dev python3-pip build-essential

COPY . /app
RUN ls -la app/

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN chmod +x boot.sh

ENTRYPOINT ["./boot.sh"]