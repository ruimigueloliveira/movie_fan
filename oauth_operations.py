import time
from typing import Tuple

from cryptography.hazmat.primitives import serialization

import statuses as s
import users_operations as u

SENTINEL = object()
# Registry entity key password
PRIV_KEY_PASSWORD = b"priv_key543"
# How many nanoseconds are there in a day
DAY_NS = int(1e9 * 60 * 60 * 24)


def _sign(*args: str):
    # Load private key
    with open("privkey.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=PRIV_KEY_PASSWORD,
        )
    # Join all strings and sign
    to_sign = bytes("".join(args), "UTF-8")
    signature = str(
        private_key.sign(to_sign), "UTF-8"
    )
    return signature


def authorization_code(username: str, email: str, password: str) -> Tuple[int, str]:
    """

    :param username:  Username
    :param email: User e-mail
    :param password: SHA256 of the user password
    :return: Authorization code that can be used to (re)generate the access token
    """

    # Check credentials
    status: int = u.check(password, username, email)
    if status != s.OK:
        return status, ""

    # -- Generate authorization code
    signature = _sign(email, password, username)
    return s.OK, signature


def access_token(auth_code: str, username: str, email: str, password: str) -> Tuple[int, str]:
    # Validate auth_token
    if not authorization_code(username, email, password)[1] == auth_code:
        # Return an error status code
        return s.INVALID_AUTH_CODE, ""
    # TODO Re-sign with deadline
    deadline = str(time.time_ns() + 30 * DAY_NS)
    return s.OK, _sign(username, email, password, deadline)


def validate_access_token(access_tkn: str) -> int:
    # TODO Decrypt w/ pub key in order to obtain the credentials and deadline
    ...
    # TODO Check if time has crossed deadline
    ...


if __name__ == '__main__':
    ...
