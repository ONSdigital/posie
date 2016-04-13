[![Build Status](https://travis-ci.org/ONSdigital/posie.svg?branch=master)](https://travis-ci.org/ONSdigital/posie)

![Logo](http://www.80snostalgia.com/files/fluposie.jpg)

# Posie

Posie is a decryption service written in Python. It is a component of the Office of National Statistics (ONS) Survey Data Exchange (SDE) project, which takes an encrypted json payload and transforms it into a number of formats for use within the ONS.

## Installation

Using virtualenv and pip, create a new environment and install within using:

    $ pip install -r requirements.txt

It's also possible to install within a container using docker. From the posie directory:

    $ docker build -t posie .

## Usage

To start posie, just run the server:

    $ python server.py

Posie exposes two endpoints '/key' and '/decrypt' which expose a public key and the decryption service respectively, by default binding to port 5000 on localhost.

The key endpoint exposes a pem format public key and the decrypt endpoint decrypts and returns the POST data it is sent as JSON. 

Posie uses [JSON Web Tokens](https://jwt.io/) to decrypt data.

### Example

The example below uses the Python library [requests](https://github.com/kennethreitz/requests) to decrypt some data using Posie.

    ```python
    import requests

    r = requests.post('http://127.0.0.1:5000/decrypt', data=encrypted_data)

    decrypted_data = r.text
    ```