import os


def get_key(key_name):
    key = open(key_name, 'r')
    contents = key.read()
    return contents


EQ_JWT_LEEWAY_IN_SECONDS = 120

# eq keys
EQ_PUBLIC_KEY = get_key(os.getenv('EQ_PUBLIC_KEY', "./keys/sdc-submission-signing-sr-public-key.pem"))

# sdx keys
PRIVATE_KEY = get_key(os.getenv('PRIVATE_KEY', "./keys/sdc-submission-encryption-sdx-private-key.pem"))

SDX_SECRETS_FILE = os.getenv('SDX_SECRETS_FILE', 'secrets.yml')
