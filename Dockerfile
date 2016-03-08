FROM iron/python:3.5.1-dev

ADD requirements.txt /app/requirements.txt
ADD server.py /app/server.py

# set working directory to /app/
WORKDIR /app/

RUN apk add --no-cache --virtual=build-dependencies libffi-dev openssl-dev g++ make python3-dev && \
    pip3 install -r requirements.txt && \
    apk del build-dependencies && \
    rm -rf /var/cache/apk/*

EXPOSE 5000

ENTRYPOINT python3 server.py