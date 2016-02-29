from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import requests
import base64

# Load public key from http endpoint

url = "http://127.0.0.1:5000/key"
r = requests.get(url)
key_string = base64.b64decode(r.content)

public_key = serialization.load_der_public_key(
    key_string,
    backend=default_backend()
)

message = b"Some encrypted message"

ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None
    )
)

r = requests.post("http://127.0.0.1:5000/import", json={
    'contents': ciphertext.decode('iso-8859-1')
})

print(str(r.text))
