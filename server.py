from flask import Flask, request, jsonify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography import exceptions

import base64
import binascii

app = Flask(__name__)

f4 = 65537

backend = default_backend()

private_key = rsa.generate_private_key(
    public_exponent=f4,
    key_size=4096,
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
        app.logger.debug("------ Received some data -------")
        app.logger.debug(request.data)
        
        decoded_msg = base64.b64decode(request.data)

        key_recvd = decoded_msg[:512]
        iv_recvd = decoded_msg[512:528]
        data_recvd = decoded_msg[528:]

        key_decrypted = private_key.decrypt(
            key_recvd,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

        cipher = Cipher(algorithms.AES(key_decrypted), modes.CTR(iv_recvd), backend=backend)

        decryptor = cipher.decryptor()
        result = decryptor.update(data_recvd) + decryptor.finalize()

        result_str = result.decode('UTF8')
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
        return result_str


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
