from flask import Flask
from sdc.crypto.secrets import KeyStore, validate_required_secrets
import yaml

import settings

EXPECTED_SECRETS = []

KEY_PURPOSE_SUBMISSION = 'submission'


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    app.sdx = {}

    with open(app.config['SDX_SECRETS_FILE']) as file:
        secrets_from_file = yaml.safe_load(file)

    validate_required_secrets(secrets_from_file, EXPECTED_SECRETS, KEY_PURPOSE_SUBMISSION)
    app.sdx['key_store'] = KeyStore(secrets_from_file)
    return app
