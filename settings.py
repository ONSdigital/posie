import os
import logging

logger = logging.getLogger(__name__)


def get_key(key_name):
    key = open(key_name, 'r')
    contents = key.read()
    return contents

EQ_JWT_LEEWAY_IN_SECONDS = 120

# EQ's keys
EQ_PUBLIC_KEY = get_key(os.getenv('EQ_PUBLIC_KEY', "/keys/sr-public.pem"))

# Posies keys
PUBLIC_KEY = get_key(os.getenv('PUBLIC_KEY', "/keys/sdx-public.pem"))
PRIVATE_KEY = get_key(os.getenv('PRIVATE_KEY', "/keys/sdx-private.pem"))
PRIVATE_KEY_PASSWORD = os.getenv("PRIVATE_KEY_PASSWORD", "digitaleq")

LOGGING_FORMAT = "%(asctime)s|%(levelname)s: %(message)s"
LOGGING_LOCATION = "error.log"
LOGGING_LEVEL = logging.DEBUG
