[![Build Status](https://travis-ci.org/ONSdigital/Posie.svg?branch=master)](https://travis-ci.org/ONSdigital/Posie)

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

The key endpoint exposes a der format public key and the decrypt endpoint decrypts and returns the POST data it is sent. 

Posie uses hybrid encryption to encrypt both the key, interupt vector and data.

### Example

The example below uses the Python libraries [cryptography](http://cryptography.io) and [requests](https://github.com/kennethreitz/requests) to encrypt some data using Posie.

1. A client first requests Posies public key
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    import os
    import base64
    import requests

    # Get the public key and load it using cryptography.io
    r = requests.get('http://127.0.0.1/5000/key', timeout=1)

    key_string = base64.b64decode(r.text)

    public_key = serialization.load_der_public_key(
        key_string,
        backend=default_backend()
    )

2. The client uses that key to encode some data. 

    # Encrypt some data using cryptography.io
    key = os.urandom(32)
    iv = os.urandom(16)

    backend = default_backend()

    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=backend)

    encryptor = cipher.encryptor()

    data = encryptor.update(unencrypted.encode('UTF8')) + encryptor.finalize()

    encrypted_key = public_key.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )

    encrypted_data = base64.b64encode(encrypted_key + iv + data)

3. The encoded data may then be passed to second client....

4. The second client may then contact Posie to decrypt the data it has been passed.

    r = requests.post('http://127.0.0.1/5000/decrypt', data=encrypted_data)

    decrypted_data = r.text

### Troubleshooting

Whilst Posie works with JSON, the service makes no assumptions on the content type sent to it. The content encrypted and decrypted with it can be json or plaintext, it's up to the calling service to convert to their desired type.

Posies public key is recreated on each server restart. Any data encrypted in the wild will need to be re-encrypted using the current public key.