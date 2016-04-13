from flask import Flask, request, jsonify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography import exceptions

from decrypter import Decrypter
import base64
import binascii
import json
import settings
import logging

app = Flask(__name__)

@app.errorhandler(400)
def known_error(error=None):
    app.logger.error("POSIE:DECRYPT:FAILURE '%s'", request.data.decode('UTF8'))
    message = {
        'status': 400,
        'message': "{}: {}".format(error, request.url),
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


@app.errorhandler(500)
def unknown_error(error=None):
    app.logger.error("POSIE:DECRYPT:FAILURE '%s'", request.data.decode('UTF8'))
    message = {
        'status': 500,
        'message': "Internal server error: " + repr(error),
    }
    resp = jsonify(message)
    resp.status_code = 500

    return resp

@app.route('/key')
def key():
    return settings.PUBLIC_KEY

@app.route('/decrypt', methods=['POST'])
def decrypt():
    request.get_data()

    if not request.data:
        return known_error("Request payload was empty")

    try:
        app.logger.debug("POSIE:DECRYPT: Received some data")
        
        data_bytes = request.data.decode('UTF8')

        decrypter = Decrypter()
        decrypted_json = decrypter.decrypt(data_bytes)
    except (
            exceptions.UnsupportedAlgorithm,
            exceptions.InvalidKey,
            exceptions.AlreadyFinalized,
            exceptions.InvalidSignature,
            exceptions.NotYetFinalized,
            exceptions.AlreadyUpdated):

        return known_error("Decryption Failure")
    except binascii.Error:
        return known_error("Request payload was not base64 encoded")
    except ValueError as e:
        if str(e) == "Ciphertext length must be equal to key size.":
            return known_error(str(e))
        elif str(e) == "Incorrect number of tokens":
            return known_error(str(e))
        else:
            return unknown_error()
    except:
        return unknown_error()
    else:
        return jsonify(**decrypted_json)


if __name__ == '__main__':
    logging.basicConfig(level=settings.LOGGING_LEVEL, format=settings.LOGGING_FORMAT)

    app.run(debug=True, host='0.0.0.0')
