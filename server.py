import os
from flask import Flask, request, json
from werkzeug import secure_filename
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64

UPLOAD_FOLDER = './ready_to_import'
DECODE_FOLDER = './decoded'

ALLOWED_EXTENSIONS = set(['ssl'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DECODE_FOLDER'] = DECODE_FOLDER

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/import', methods=['POST'])
def receiver():
    file = request.files['encoded']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.close()

        f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')
        ciphertext = f.read()
        f.close()

        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        ).decode(encoding="UTF-8")

        decoded = open(os.path.join(app.config['DECODE_FOLDER'], "%s.decoded.txt" % filename), 'w')
        decoded.write(plaintext)
        decoded.close()

        return json.dumps({
            "success": True,
            "data": plaintext
        })

    return json.dumps({
        "success": False
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
