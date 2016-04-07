import os
import logging

logger = logging.getLogger(__name__)

def get_key(key_name):
    """
    TODO remove these once the encrypted key story is finished
    :return:
    """
    logger.debug("Opening file %", key_name)
    key = open(key_name, 'r')
    contents = key.read()
    logger.debug("Key is %s", contents)
    return contents

EQ_JWT_LEEWAY_IN_SECONDS = 120

PUBLIC_KEY = get_key(os.getenv('PUBLIC_KEY', "./jwt-test-keys/sdx-public.pem"))
PRIVATE_SIGNING_KEY = get_key(os.getenv('PRIVATE_SIGNING_KEY', "./jwt-test-keys/sdx-private.pem"))
PRIVATE_SIGNING_KEY_PASSWORD = os.getenv("PRIVATE_SIGNING_KEY_PASSWORD", "digitaleq")