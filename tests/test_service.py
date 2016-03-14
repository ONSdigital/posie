from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

import base64
import unittest
import sys
import os

sys.path.append(os.path.abspath('../server.py'))

import server


class TestPosieService(unittest.TestCase):

    def test_key_generation(self):
        # Load public der key from http endpoint

        key_string = base64.b64decode(server.key())

        public_key = serialization.load_der_public_key(
            key_string,
            backend=default_backend()
        )

        self.assertIsNotNone(public_key)
