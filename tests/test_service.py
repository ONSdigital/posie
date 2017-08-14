import base64
import json
import os
import unittest

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from sdc.crypto.key_store import KeyStore
import jwt
import yaml

from tests import create_keys
create_keys()  # NOQA - generate the keys before the tests run and it needs to be done before importing server

import settings
from server import app
from server import KEY_PURPOSE_SUBMISSION


def get_key(key_name):
    key = open(key_name, 'r')
    contents = key.read()
    return contents


# sdx keys
PRIVATE_KEY = get_key("./jwt-test-keys/sdc-sdx-submission-encryption-private-v1.pem")
TEST_EQ_PRIVATE_KEY = get_key("./jwt-test-keys/sdc-eq-submission-signing-private-v1.pem")


class Encrypter:
    def __init__(self, private_kid, public_kid):
        self.private_kid = private_kid
        self.public_kid = public_kid

        private_key_bytes = self._to_bytes(TEST_EQ_PRIVATE_KEY)

        self.private_key = serialization.load_pem_private_key(private_key_bytes,
                                                              password=None,
                                                              backend=backend)
        private_decryption_key = serialization.load_pem_private_key(
            PRIVATE_KEY.encode(),
            password=None,
            backend=backend
        )

        public_key_bytes = private_decryption_key.public_key().public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        )

        self.public_key = serialization.load_pem_public_key(public_key_bytes, backend=backend)

        # first generate a random key
        self.cek = os.urandom(32)  # 256 bit random CEK

        # now generate a random IV
        self.iv = os.urandom(12)  # 96 bit random IV

    @classmethod
    def _to_bytes(self, bytes_or_str):
        if isinstance(bytes_or_str, str):
            value = bytes_or_str.encode()
        else:
            value = bytes_or_str
        return value

    def _jwe_protected_header(self):
        header = '{"alg":"RSA-OAEP","enc":"A256GCM", "kid":"' + self.private_kid + '"}'
        return self._base_64_encode(header.encode())

    def _encrypted_key(self, cek):
        ciphertext = self.public_key.encrypt(cek, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))
        return self._base_64_encode(ciphertext)

    def _encode_iv(self, iv):
        return self._base_64_encode(iv)

    @classmethod
    def _base_64_encode(self, text):
        # strip the trailing = as they are padding to make the result a multiple of 4
        # the RFC does the same, as do other base64 libraries so this is a safe operation
        return base64.urlsafe_b64encode(text).decode().strip("=").encode()

    def _encode_and_signed(self, payload):
        return jwt.encode(payload, self.private_key, algorithm="RS256", headers={'kid': self.public_kid, 'typ': 'jwt'})

    def encrypt(self, json):
        payload = self._encode_and_signed(json)
        jwe_protected_header = self._jwe_protected_header()
        encrypted_key = self._encrypted_key(self.cek)

        cipher = Cipher(algorithms.AES(self.cek), modes.GCM(self.iv), backend=backend)
        encryptor = cipher.encryptor()

        encryptor.authenticate_additional_data(jwe_protected_header)

        ciphertext = encryptor.update(payload) + encryptor.finalize()

        tag = encryptor.tag

        encoded_ciphertext = self._base_64_encode(ciphertext)
        encoded_tag = self._base_64_encode(tag)

        # assemble result
        jwe = jwe_protected_header + b"." + encrypted_key + b"." + self._encode_iv(self.iv) + b"." + encoded_ciphertext + b"." + encoded_tag

        return jwe


class TestDecryptService(unittest.TestCase):

    decrypt_endpoint = "/decrypt"

    def setUp(self):
        # creates a test client
        self.app = app.test_client()

        # propagate the exceptions to the test client
        self.app.testing = True
        with open(settings.SDX_KEYS_FILE) as file:
            secrets_from_file = yaml.safe_load(file)

        secret_store = KeyStore(secrets_from_file)

        jwt_key = secret_store.get_key_for_purpose_and_type(KEY_PURPOSE_SUBMISSION, "private")

        jwe_key = secret_store.get_key_for_purpose_and_type(KEY_PURPOSE_SUBMISSION, "public")

        self.encrypter = Encrypter(jwt_key.kid, jwe_key.kid)

    def encrypt_and_send_json(self, json_string):

        data = json.loads(json_string)

        encoded_data = self.encrypter.encrypt(data)

        # Ask posie to decode message
        r = self.app.post(self.decrypt_endpoint, data=encoded_data)

        return r

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
        message = '''{"some": "well", "formed": "json"}'''

        # Ask posie to decode message
        r = self.encrypt_and_send_json(message)

        # Compare to bytestring version of decrypted data
        self.assertEqual(json.loads(r.data.decode('UTF8')), json.loads(message))

    def test_decrypts_large_message_no_tx_id(self):
        # Encrypt a message with the key
        message = '''{
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

        # Encrypt and ask posie to decode message
        r = self.encrypt_and_send_json(message)

        self.assertEqual(json.loads(r.data.decode('UTF8')), json.loads(message))

    def test_decrypts_large_message_with_tx_id(self):
        # Encrypt a message with the key
        message = '''{
            "type": "uk.gov.ons.edc.eq:surveyresponse",
            "version": "0.0.1",
            "origin": "uk.gov.ons.edc.eq",
            "survey_id": "21",
            "tx_id": "27923934-62de-475c-bc01-433c09fd38b8",
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

        # Encrypt and ask posie to decode message
        r = self.encrypt_and_send_json(message)

        self.assertEqual(json.loads(r.data.decode('UTF8')), json.loads(message))
