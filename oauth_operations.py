from typing import Tuple
import cryptography

import statuses
import users_operations as u

SENTINEL = object()
# Registry entity key pair
PRIV_KEY: str = "priv_key543"
PUB_KEY: str = "pub_key546"


def authorization_code(username: str, email: str, password: str) -> Tuple[int, str]:
    # Check credentials
    status: int = u.check(password, username, email)
    if status != statuses.OK:
        return status, ""
    # TODO join all strings and sign
    ...


def access_token(auth_code: str, username: str, email: str, password: str) -> Tuple[int, str]:
    # Validate auth_token
    if not authorization_code(username, email, password)[1] == auth_code:
        # TODO Return an error status code
        ...
    # TODO Re-sign w/ time.time_ns()
    ...


def validate_access_token(access_tkn: str) -> int:
    # TODO Decrypt w/ pub key in order to obtain the credentials and deadline
    ...
    # TODO Check if time has crossed deadline
    ...


if __name__ == '__main__':
    ...
