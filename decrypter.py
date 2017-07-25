from sdc.crypto.decrypter import decrypt


class Decrypter(object):

    def decrypt(self, token, secret_store):
        tokens = token.split('.')
        if len(tokens) != 5:
            raise ValueError("Incorrect number of tokens")
        return decrypt(token, secret_store)
