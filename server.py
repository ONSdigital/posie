from flask import Flask, request, jsonify, g
from cryptography import exceptions
from decrypter import Decrypter
from structlog import wrap_logger
import binascii
import logging
import os
import yaml
import settings
from secrets import SecretStore

from sdx.common.logger_config import logger_initial_config


__version__ = "1.3.0"


EXPECTED_SECRETS = [
    "SDX_SECRET_KEY",
]

KEY_PURPOSE_SUBMISSION = 'eq-submission'


def validate_required_submission_keys(secrets):
    found_submission_public = False
    found_submission_private = False

    for kid in secrets['keys']:
        key = secrets['keys'][kid]
        if key['purpose'] == KEY_PURPOSE_SUBMISSION:
            if key['type'] == 'public':
                if found_submission_public:
                    raise Exception("Multiple public submission keys loaded")
                else:
                    found_submission_public = True

            if key['type'] == 'private':
                if found_submission_private:
                    raise Exception("Multiple private submission keys loaded")
                else:
                    found_submission_private = True

    if not found_submission_public:
        raise Exception("No public submission key loaded")

    if not found_submission_private:
        raise Exception("No private submission key loaded")


def validate_required_secrets(secrets):
    for required_secret in EXPECTED_SECRETS:
        if required_secret not in secrets['secrets']:
            raise Exception("Missing Secret [{}]".format(required_secret))

    validate_required_submission_keys(secrets)

app = Flask(__name__)
app.config.from_object(settings)

app.sdx = {}

secrets = yaml.safe_load(open(app.config['SDX_SECRETS_FILE']))
validate_required_secrets(secrets)
app.sdx['secret_store'] = SecretStore(secrets)

logger_initial_config(service_name='sdx-decrypt')

logger = wrap_logger(
    logging.getLogger(__name__)
)
logger.info("START", version=__version__)



def get_decrypter():
    # Sets up a single decrypter throughout app.
    decrypter = getattr(g, '_decrypter', None)
    if decrypter is None:
        try:
            decrypter = g._decrypter = Decrypter()
        except Exception as e:
            logger.error("Decrypter failed to start", exception=repr(e))

    return decrypter


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
        decrypter = get_decrypter()
        decrypted_json = decrypter.decrypt(data_bytes)
    except (
            exceptions.UnsupportedAlgorithm,
            exceptions.InvalidKey,
            exceptions.AlreadyFinalized,
            exceptions.InvalidSignature,
            exceptions.NotYetFinalized,
            exceptions.AlreadyUpdated):

        return client_error("Decryption Failure")
    except binascii.Error:
        return client_error("Request payload was not base64 encoded")
    except ValueError as e:
        if str(e) == "Ciphertext length must be equal to key size.":
            return client_error(str(e))
        elif str(e) == "Incorrect number of tokens":
            return client_error(str(e))
        else:
            return server_error(e)
    except Exception as e:
        return server_error(e)
    else:
        bound_logger = logger.bind(tx_id=decrypted_json.get("tx_id"))
        bound_logger.info("Decrypted received data")
        return jsonify(**decrypted_json)


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
