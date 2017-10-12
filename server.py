import binascii
import logging
import os

from cryptography import exceptions
from flask import current_app, request, jsonify
from sdc.crypto.decrypter import decrypt as sdc_decrypt
from sdc.crypto.exceptions import InvalidTokenException
from sdx.common.logger_config import logger_initial_config
from structlog import wrap_logger

from application import create_app, KEY_PURPOSE_SUBMISSION


__version__ = "1.4.0"

logger_initial_config(service_name='sdx-decrypt')

logger = wrap_logger(
    logging.getLogger(__name__)
)
logger.info("START", version=__version__)

app = create_app()


@app.errorhandler(400)
def errorhandler_400(e):
    return client_error(repr(e))


def client_error(error=None):
    logger.error(repr(error))
    message = {
        'status': 400,
        'message': repr(error),
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
        decrypted_json = sdc_decrypt(
            data_bytes, current_app.sdx['key_store'], KEY_PURPOSE_SUBMISSION)
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
        logger.exception(repr(e))
        return client_error(e)
    except ValueError as e:
        logger.exception(repr(e))
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
