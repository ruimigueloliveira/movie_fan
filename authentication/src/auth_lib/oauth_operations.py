"""Provides basic functionality based on the OAuth standard.

"""

import os.path
import time
from typing import Tuple, Union, Optional

import cryptography.hazmat.backends
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

import auth_lib.db_operations
from auth_lib import statuses as s

# Registry entity key
PRIVATE_KEY_PEM = "auth_private_key.pem"

password_filepath = os.path.join(os.path.dirname(__file__), "password")
try:
    with open(password_filepath, mode="r") as f:
        PRIVATE_KEY_PASSWORD = bytes(f.readlines()[0], "utf-8")
except FileNotFoundError:
    print(f"Error: Password file should be in path \"{password_filepath}\"!")
    exit(1)

# How many nanoseconds are there in a day
DAY_NS = int(1e9 * 60 * 60 * 24)  # 60s * 60 min * 24h
# Separates the arguments when encrypting multiple strings
SEPARATOR: str = ';'


def _load_priv_key() -> RSAPrivateKey:
    """Load the private key of the authentication entity

    :return: Private key of the authentication entity
    """
    # Load private key
    with open(os.path.join(os.path.dirname(__file__), PRIVATE_KEY_PEM), "rb") as key_file:
        try:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=PRIVATE_KEY_PASSWORD,
                backend=cryptography.hazmat.backends.default_backend()
            )
        except ValueError:
            print(f"Password \"{PRIVATE_KEY_PASSWORD}\" is incorrect.")
            exit(1)
    return private_key


def _sign(*args: str) -> bytes:
    """Joins multiple strings and signs them

    :param args: Multiple string messages
    :return: Bytes form of the signature
    """
    private_key = _load_priv_key()
    # Join all strings and sign
    to_sign = bytes(SEPARATOR.join(args), "UTF-8")
    signature: bytes = private_key.sign(
        to_sign,
        padding=padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        algorithm=hashes.SHA256()
    )
    return signature


def _verify(signature: bytes, *args: Union[str, bytes]) -> bool:
    """Verify signature against provided data

    :param signature: Signature produced by this module
    :param args: String of strings or a single bytes object
    :return: True if the signature is authentic, False otherwise.
    """
    # TODO (low prio.) add verification for args parameter

    # If args.len == 1, element must be bytes, elements otherwise
    data = SEPARATOR.join(args).encode("utf-8") if len(args) > 1 else args[0]

    try:
        # Get public key
        pub_key = _load_priv_key().public_key()
        # Verify signature
        pub_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False


def authorization_code(username: str, email: Optional[str], password: str) -> Tuple[int, bytes]:
    """Generates the OAuth authorization token.

    Token is a signature of the credentials.

    :param username: Username
    :param email: User e-mail
    :param password: User password
    :return: Status code; Authorization code that can be used to (re)generate the access token
    """

    # Check credentials
    status: int = auth_lib.db_operations.check(password, username, email)
    if status != s.OK:
        return status, b""

    if email is None:
        return s.OK, _sign(password, username)

    # -- Generate authorization code
    signature = _sign(email, password, username)
    return s.OK, signature


def generate_access_token(auth_code: bytes, username: str, email: str, password: str) -> Tuple[int, bytes]:
    """Generates the OAuth access token

    Token is a signature of the authorization code (hex) concatenated
     with the deadline for the validity.

    :param auth_code: Authorization code obtained with the function of this module
    :param username: Username
    :param email: User e-mail
    :param password: User password
    :return: Status code; Access code in bytes form (utf-8)
    """
    # Verify auth_token
    if _verify(auth_code, email, password, username) is True:
        # Re-sign with deadline
        deadline_ns = str(time.time_ns() + 30 * DAY_NS)
        return s.OK, _sign(auth_code.hex()) + f"-ds{deadline_ns}".encode(encoding="UTF-8")
    else:
        return s.INVALID_AUTH_CODE, b""


def validate_access_token(access_tkn: bytes, auth_tkn: bytes) -> int:
    """Validates the access token

    Validation is performed against the authorization code as well as
     evaluates the deadline in the token against the current time

    :param access_tkn: Access token
    :param auth_tkn: Authorization token
    :return: Status code of the validation - 0 if valid, > 0 otherwise
    """

    # Extract signature and deadline
    token, deadline = access_tkn.split(b"-ds")
    # Verify signature part of the access token against the authorization token
    if not _verify(token, auth_tkn):
        return s.INVALID_ACCESS_TOKEN
    # Obtain the credentials and deadline
    deadline_ns = int(deadline)
    # Check if time has crossed deadline
    if deadline_ns < time.time_ns():
        return s.OVERDUE_ACCESS_TOKEN
    return s.OK


if __name__ == '__main__':
    # Generate authorization code
    status_code, auth = authorization_code(username="andre", email="andre@gmail.com", password="andre$P1")
    assert status_code == 0, f"Authorization code error code {status_code}: {s.status_description(status_code)}"

    # Generate access token
    status_code, access_token = generate_access_token(
        auth_code=auth, username="andre", email="andre@gmail.com", password="andre$P1"
    )
    assert status_code == 0, f"Access token generation error code {status_code}: {s.status_description(status_code)}"

    # Validate access token
    status_code = validate_access_token(access_tkn=access_token, auth_tkn=auth)
    assert status_code == 0, f"Access token validation error code {status_code}: {s.status_description(status_code)}"
