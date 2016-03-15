from flask import Flask, request, jsonify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography import exceptions
import base64
import binascii

app = Flask(__name__)

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072,
    backend=default_backend()
)


@app.errorhandler(400)
def known_error(error=None):
    message = {
        'status': 400,
        'message': "{}: {}".format(error, request.url),
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


@app.errorhandler(500)
def unknown_error():
    message = {
        'status': 500,
        'message': "Internal server error",
    }
    resp = jsonify(message)
    resp.status_code = 500

    return resp


@app.route('/key')
def key():

    key = private_key.public_key().public_bytes(
        encoding=Encoding.DER,
        format=PublicFormat.SubjectPublicKeyInfo
    )

    return base64.b64encode(key)


@app.route('/decrypt', methods=['POST'])
def receiver():
    request.get_data()

    if not request.data:
        return known_error("Request payload was empty")

    try:
        encoded_json = request.data

        plaintext = private_key.decrypt(
            base64.b64decode(encoded_json),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        ).decode(encoding="UTF-8")
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
        else:
            return unknown_error()
    except:
        return unknown_error()
    else:
        return plaintext


if __name__ == '__main__':
    app.run(host='0.0.0.0')
