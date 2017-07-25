#!/usr/bin/env python

import argparse

from sdc.crypto.scripts.generate_secrets import add_private_key_to_dict, add_public_key_to_dict, get_file_contents, generate_secrets_file

KEY_PURPOSE_EQ_SUBMISSION = 'eq-submission'


def generate_secrets_for_sdx(keys_folder):
    keys = {}

    add_private_key_to_dict(keys, KEY_PURPOSE_EQ_SUBMISSION, 'sdc-submission-encryption-sdx-private-key.pem', keys_folder)
    add_public_key_to_dict(keys, KEY_PURPOSE_EQ_SUBMISSION, 'sdc-submission-signing-sr-public-key.pem', keys_folder)

    secrets = {}

    secrets['SDX_SECRET_KEY'] = get_file_contents(keys_folder, 'sdx-secret-key.txt', True)

    generate_secrets_file(keys, secrets)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate Survery Data Exchange secrets file.')
    parser.add_argument('folder', type=str,
                        help='The folder that contains the secrets and keys')

    args = parser.parse_args()

    keys_folder = args.folder
    generate_secrets_for_sdx(keys_folder)
