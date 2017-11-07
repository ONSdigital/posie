import os
import logging

SDX_KEYS_FILE = os.getenv('SDX_KEYS_FILE', 'jwt-test-keys/keys.yml')

LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'DEBUG'))
LOGGING_FORMAT = "%(asctime)s.%(msecs)06dZ|%(levelname)s: sdx-decrypt: %(message)s"
