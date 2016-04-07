FROM iwootten/flask-crypto

ADD server.py /app/server.py
ADD settings.py /app/settings.py
ADD decrypter.py /app/decrypter.py
ADD jwt-test-keys /app/jwt-test-keys

# set working directory to /app/
WORKDIR /app/

EXPOSE 5000

ENTRYPOINT python3 server.py