from flask import Flask, request, jsonify, g
from cryptography import exceptions
from decrypter import Decrypter
from structlog import wrap_logger
import binascii
import settings
import logging
import sys
import os


app = Flask(__name__)

logging.basicConfig(stream=sys.stdout, level=settings.LOGGING_LEVEL, format=settings.LOGGING_FORMAT)
logger = wrap_logger(
    logging.getLogger(__name__)
)
logger.debug("START")


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
    logger.error(error, request=request.data.decode('UTF8'))
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
    logger.error("Server Error", exception=repr(e), request=request.data.decode('UTF8'))
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
        logger.debug("Received some data")
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
        return jsonify(**decrypted_json)


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    port = int(os.getenv("PORT"))
    app.run(debug=True, host='0.0.0.0', port=port)
