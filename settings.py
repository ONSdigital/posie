import os
import logging

logger = logging.getLogger(__name__)


def get_key(key_name):
    key = open(key_name, 'r')
    contents = key.read()
    return contents

EQ_JWT_LEEWAY_IN_SECONDS = 120

# EQ's keys
EQ_PUBLIC_KEY = get_key(os.getenv('EQ_PUBLIC_KEY', "/keys/sdc-submission-signing-sr-public-key.pem"))

# Posies keys
PRIVATE_KEY = get_key(os.getenv('PRIVATE_KEY', "/keys/sdc-submission-encryption-sdx-private-key.pem"))
PRIVATE_KEY_PASSWORD = os.getenv("PRIVATE_KEY_PASSWORD", "digitaleq")

LOGGING_FORMAT = "%(asctime)s|%(levelname)s: %(message)s"
LOGGING_LOCATION = "logs/error.log"
LOGGING_LEVEL = logging.DEBUG
