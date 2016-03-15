from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from server import app
import base64
import unittest


class TestPosieService(unittest.TestCase):

    key_endpoint = "/key"
    decrypt_endpoint = "/decrypt"

    def setUp(self):
        # creates a test client
        self.app = app.test_client()

        # propagate the exceptions to the test client
        self.app.testing = True

        r = self.app.get(self.key_endpoint)

        key_string = base64.b64decode(r.data)

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
        r = self.app.post(self.decrypt_endpoint, data=base64.b64encode(ciphertext))

        return r

    def test_key_generation(self):
        self.assertIsNotNone(self.public_key)

    def test_decrypt_fail_sends_400(self):

        # Ask posie to decode message
        r = self.app.post(self.decrypt_endpoint, data='rubbish')

        self.assertEqual(r.status_code, 400)

    def test_no_content_sends_400(self):

        # Ask posie to decode message
        r = self.app.post(self.decrypt_endpoint, data='')

        self.assertEqual(r.status_code, 400)

    def test_decrypts_message(self):
        # Encrypt a message with the key
        message = b"Some encrypted message"

        # Ask posie to decode message
        r = self.send_message(message)

        # Compare to bytestring version of decrypted data
        self.assertEqual(r.data, message)

    def test_decrypts_large_message(self):
        # Encrypt a message with the key
        message = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut lectus urna, elementum vitae massa congue, varius aliquam purus. Etiam quis pellentesque felis. Morbi vehicula sagittis enim iaculis pretium. Fusce venenatis pretium ante, et semper ipsum blandit vitae. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras lobortis dictum sapien et faucibus. Nulla vitae nisl ante."

        # Ask posie to decode message
        r = self.send_message(message)

        # Compare to bytestring version of decrypted data
        self.assertEqual(r.data, message)
