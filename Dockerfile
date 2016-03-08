FROM ubuntu:latest

ADD requirements.txt /app/requirements.txt
ADD server.py /app/server.py

# set working directory to /app/
WORKDIR /app/

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential libffi-dev python3-pip python3-dev libssl-dev && \
    pip3 install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 5000

ENTRYPOINT python3 server.py