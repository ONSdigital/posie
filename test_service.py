from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import os
import requests

# Load public key from http endpoint

url = "http://192.168.99.100/key"
r = requests.get(url)
key_string = r.content

public_key = serialization.load_pem_public_key(
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

encoded = open(os.path.join("./data", "encoded.ssl"), 'w')
encoded.write(ciphertext)
encoded.close()

files = {'encoded': open(os.path.join("./data", "encoded.ssl"), 'rb')}

r = requests.post("http://192.168.99.100/import", files=files)

print r.text
