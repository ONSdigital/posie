from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import requests
import base64
import unittest
import json


class TestPosieService(unittest.TestCase):

    key_url = "http://127.0.0.1:5000/key"
    import_url = "http://127.0.0.1:5000/import"
    public_key = ""

    def setUp(self):
        # Load public der key from http endpoint

        r = requests.get(self.key_url)
        key_string = base64.b64decode(r.content)

        self.public_key = serialization.load_der_public_key(
            key_string,
            backend=default_backend()
        )

    def test_decrypts_message(self):
        # Encrypt a message with the key
        message = b"Some encrypted message"

        ciphertext = self.public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

        # Ask posie to decode message
        r = requests.post(self.import_url, json={
            'contents': ciphertext.decode('iso-8859-1')
        })
        json_data = json.loads(r.text)
        self.assertEquals(json_data['data'], message)
