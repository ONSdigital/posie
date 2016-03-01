from flask import Flask, request, json
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


@app.route('/key')
def key():

    key = private_key.public_key().public_bytes(
        encoding=Encoding.DER,
        format=PublicFormat.SubjectPublicKeyInfo
    )

    return base64.b64encode(key)


@app.route('/import', methods=['POST'])
def receiver():
    try:
        posted_json = request.get_json()
        encoded_json = posted_json.get('contents').encode('utf-8')

        plaintext = private_key.decrypt(
            base64.b64decode(encoded_json),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        ).decode(encoding="UTF-8")

        return json.dumps({
            "success": True,
            "data": plaintext
        })
    except:
        return json.dumps({
            "success": False
        })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
