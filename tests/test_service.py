from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from server import app
import base64
import unittest
import os


class TestPosieService(unittest.TestCase):

    key_endpoint = "/key"
    decrypt_endpoint = "/decrypt"

    def setUp(self):
        self.key = os.urandom(32)
        self.iv = os.urandom(16)

        backend = default_backend()

        cipher = Cipher(algorithms.AES(self.key), modes.CTR(self.iv), backend=backend)

        self.encryptor = cipher.encryptor()

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

    def send_message(self, message_bytes):
        data = self.encryptor.update(message_bytes) + self.encryptor.finalize()

        encrypted_key = self.public_key.encrypt(
            self.key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

        encoded_data = base64.b64encode(encrypted_key + self.iv + data)

        # Ask posie to decode message
        r = self.app.post(self.decrypt_endpoint, data=encoded_data)

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
        message = b'''{
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "version": "0.0.1",
            "origin": "uk.gov.ons.edc.eq",
            "survey_id": "21",
            "collection": {
              "exercise_sid": "hfjdskf",
              "instrument_id": "0203",
              "period": "2016-02-01"
            },
            "submitted_at": "2016-03-12T10:39:40Z",
            "metadata": {
              "user_id": "789473423",
              "ru_ref": "12345678901A"
            },
            "data": {
              "11": "01042016",
              "12": "31102016",
              "20": "1800000",
              "51": "84",
              "52": "10",
              "53": "73",
              "54": "24",
              "50": "205",
              "22": "705000",
              "23": "900",
              "24": "74",
              "25": "50",
              "26": "100",
              "21": "60000",
              "27": "7400",
              "146": "some comment"
            }
        }'''

        # Ask posie to decode message
        r = self.send_message(message)

        # Compare to bytestring version of decrypted data
        self.assertEqual(r.data, message)
