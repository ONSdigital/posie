from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

import requests
import base64
import unittest
import os


class TestPosieService(unittest.TestCase):

    POSIE_URL = os.getenv('POSIE_URL', 'http://127.0.0.1:5000')

    key_url = "{}/key".format(POSIE_URL)
    import_url = "{}/decrypt".format(POSIE_URL)
    public_key = ""

    def setUp(self):
        # Load public der key from http endpoint

        r = requests.get(self.key_url)

        key_string = base64.b64decode(r.text)

        self.public_key = serialization.load_der_public_key(
            key_string,
            backend=default_backend()
        )

    def send_message(self, message):

        ciphertext = self.public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

        # Ask posie to decode message
        r = requests.post(self.import_url, data=base64.b64encode(ciphertext))

        return r

    def test_decrypt_fail_sends_400(self):

        # Ask posie to decode message
        r = requests.post(self.import_url, data='rubbish')

        self.assertEqual(r.status_code, 400)

    def test_no_content_sends_400(self):

        # Ask posie to decode message
        r = requests.post(self.import_url, data='')

        self.assertEqual(r.status_code, 400)

    def test_decrypts_message(self):
        # Encrypt a message with the key
        message = b"Some encrypted message"

        # Ask posie to decode message
        r = self.send_message(message)

        # Compare to bytestring version of decrypted data
        self.assertEqual(str.encode(r.text), message)
