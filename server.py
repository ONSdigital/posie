import binascii
import logging
import os

from cryptography import exceptions
from flask import Flask, request, jsonify
from sdc.crypto.decrypter import decrypt as sdc_decrypt
from sdc.crypto.invalid_token_exception import InvalidTokenException
from sdc.crypto.secrets import SecretStore, validate_required_secrets
from sdx.common.logger_config import logger_initial_config
from structlog import wrap_logger
import yaml

import settings

EXPECTED_SECRETS = [
    "SDX_SECRET_KEY",
]

KEY_PURPOSE_SUBMISSION = 'eq-submission'


__version__ = "1.3.0"


app = Flask(__name__)
app.config.from_object(settings)

app.sdx = {}

with open(app.config['SDX_SECRETS_FILE']) as file:
    secrets_from_file = yaml.safe_load(file)

validate_required_secrets(secrets_from_file, EXPECTED_SECRETS, KEY_PURPOSE_SUBMISSION)
app.sdx['secret_store'] = SecretStore(secrets_from_file)

logger_initial_config(service_name='sdx-decrypt')

logger = wrap_logger(
    logging.getLogger(__name__)
)
logger.info("START", version=__version__)


@app.errorhandler(400)
def errorhandler_400(e):
    return client_error(repr(e))


def client_error(error=None):
    logger.error(error)
    message = {
        'status': 400,
        'message': error,
        'uri': request.url
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


@app.errorhandler(500)
def server_error(e):
    logger.error("Server Error", exception=repr(e))
    message = {
        'status': 500,
        'message': "Internal server error: " + repr(e)
    }
    resp = jsonify(message)
    resp.status_code = 500

    return resp


@app.route('/decrypt', methods=['POST'])
def decrypt():
    request.get_data()

    if not request.data:
        return client_error("Request payload was empty")

    try:
        logger.info("Received some data")
        data_bytes = request.data.decode('UTF8')
        decrypted_json = sdc_decrypt(data_bytes, app.sdx['secret_store'], KEY_PURPOSE_SUBMISSION)
    except (
            exceptions.UnsupportedAlgorithm,
            exceptions.InvalidKey,
            exceptions.AlreadyFinalized,
            exceptions.InvalidSignature,
            exceptions.NotYetFinalized,
            exceptions.AlreadyUpdated):

        return client_error("Decryption Failure")
    except binascii.Error as e:
        logger.exception(e)
        return client_error("Request payload was not base64 encoded")
    except InvalidTokenException as e:
        logger.exception(e)
        return client_error(str(e))
    except ValueError as e:
        logger.exception(e)
        if str(e) == "Ciphertext length must be equal to key size.":
            return client_error(str(e))
        elif str(e) == "Incorrect number of tokens":
            return client_error(str(e))
        else:
            return server_error(e)
    except Exception as e:
        logger.exception(e)
        return server_error(e)
    else:
        bound_logger = logger.bind(tx_id=decrypted_json.get("tx_id"))
        bound_logger.info("Decrypted received data")
        return jsonify(**decrypted_json)


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    port = int(os.getenv("PORT"))
    app.run(debug=True, host='0.0.0.0', port=port)
