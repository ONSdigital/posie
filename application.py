from flask import Flask
from sdc.crypto.key_store import KeyStore, validate_required_keys
import yaml

import settings

EXPECTED_SECRETS = []

KEY_PURPOSE_SUBMISSION = 'submission'


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    app.sdx = {}

    with open(app.config['SDX_KEYS_FILE']) as file:
        keys = yaml.safe_load(file)

    validate_required_keys(keys, KEY_PURPOSE_SUBMISSION)
    app.sdx['key_store'] = KeyStore(keys)
    return app
