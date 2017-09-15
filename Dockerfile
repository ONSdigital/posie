FROM onsdigital/flask-crypto

COPY application.py /app/application.py
COPY server.py /app/server.py
COPY settings.py /app/settings.py
COPY startup.sh /app/startup.sh
COPY requirements.txt /app/requirements.txt

# set working directory to /app/
WORKDIR /app/

EXPOSE 5000

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -yq git gcc make build-essential python3-dev python3-reportlab

RUN pip3 install --no-cache-dir -U -r requirements.txt

ENTRYPOINT ./startup.sh
