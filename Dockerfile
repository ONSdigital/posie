FROM onsdigital/flask-crypto

COPY application.py /app/application.py
COPY server.py /app/server.py
COPY settings.py /app/settings.py
COPY startup.sh /app/startup.sh
COPY requirements.txt /app/requirements.txt
COPY Makefile /app/Makefile

# set working directory to /app/
WORKDIR /app/

EXPOSE 5000

RUN make build

ENTRYPOINT ./startup.sh
