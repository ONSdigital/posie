from flask import Flask, request, jsonify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64

app = Flask(__name__)

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072,
    backend=default_backend()
)


@app.errorhandler(500)
def decryption_error(error=None):
    message = {
        'status': 500,
        'message': 'Decryption Failure: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 500

    return resp


@app.errorhandler(400)
def empty_content(error=None):
    message = {
        'status': 400,
        'message': 'Empty content: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 400

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
        return empty_content()
    else:
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

            return plaintext
        except:
            return decryption_error()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
