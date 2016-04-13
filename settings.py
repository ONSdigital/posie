import os
import logging

def get_key(key_name):
    key = open(key_name, 'r')
    contents = key.read()
    return contents

EQ_JWT_LEEWAY_IN_SECONDS = 120

# EQ's keys
EQ_PUBLIC_KEY = get_key(os.getenv('PUBLIC_KEY', "./jwt-test-keys/sr-public.pem"))
EQ_PRIVATE_KEY = get_key(os.getenv('PUBLIC_KEY', "./jwt-test-keys/sr-private.pem"))

# Posies keys
PUBLIC_KEY = get_key(os.getenv('PRIVATE_KEY', "./jwt-test-keys/sdx-public.pem"))
PRIVATE_KEY = get_key(os.getenv('PRIVATE_KEY', "./jwt-test-keys/sdx-private.pem"))
PRIVATE_KEY_PASSWORD = os.getenv("PRIVATE_KEY_PASSWORD", "digitaleq")

LOGGING_FORMAT = "%(asctime)s|%(levelname)s: %(message)s"
LOGGING_LOCATION = "error.log"
LOGGING_LEVEL = logging.debug