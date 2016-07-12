FROM onsdigital/flask-crypto

ADD server.py /app/server.py
ADD settings.py /app/settings.py
ADD decrypter.py /app/decrypter.py
ADD startup.sh /app/startup.sh

# set working directory to /app/
WORKDIR /app/

EXPOSE 5000

ENTRYPOINT ./startup.sh