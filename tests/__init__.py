import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption

from sdc.crypto.scripts.generate_keys import generate_keys


def create_keys():

    f4 = 65537

    eq_private_key = rsa.generate_private_key(
        public_exponent=f4,
        key_size=3072,
        backend=default_backend()
    )

    eq_private_bytes = eq_private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=NoEncryption()
    )

    eq_public_key = eq_private_key.public_key().public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo
    )

    if not os.path.exists('./jwt-test-keys'):
        os.mkdir('./jwt-test-keys')

    f = open('./jwt-test-keys/sdc-submission-signing-sr-public-key.pem', 'w')
    f.write(eq_public_key.decode('UTF8'))
    f.close()

    f = open('./jwt-test-keys/sdc-submission-signing-sr-private-key.pem', 'w')
    f.write(eq_private_bytes.decode('UTF8'))
    f.close()

    sde_private_key = rsa.generate_private_key(
        public_exponent=f4,
        key_size=3072,
        backend=default_backend()
    )

    sde_private_bytes = sde_private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=NoEncryption()
    )

    f = open('./jwt-test-keys/sdc-submission-encryption-sdx-private-key.pem', 'w')
    f.write(sde_private_bytes.decode('UTF8'))
    f.close()

    generate_keys("jwt-test-keys")
