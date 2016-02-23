FROM python:2.7

ADD requirements.txt /app/requirements.txt
ADD server.py /app/server.py

# set working directory to /app/
WORKDIR /app/

RUN mkdir /app/ready_to_import
RUN mkdir /app/decoded

# install python dependencies
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT python server.py