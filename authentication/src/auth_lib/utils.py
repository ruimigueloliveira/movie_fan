"""Provides operations for checking the validity of the credentials' parameters

"""

import hashlib
import re

# --- Constants ---
# Sentinel design pattern
import string

from auth_lib.statuses import OK, INVALID_USERNAME, INVALID_EMAIL, VALID_PASSWORD, \
    PASSWORD_TOO_SHORT, \
    PASSWORD_TOO_LONG, PASSWORD_NO_NUMBERS, PASSWORD_NO_UPPERCASE, PASSWORD_NO_LOWERCASE, PASSWORD_NO_SPECIAL_SYMBOLS, \
    SPECIAL_SYM, PASSWORD_INVALID_SYMBOLS

SENTINEL = object()


def hash_unicode(a_string: str) -> str:
    """Hashes an utf-8 string

    Reference: https://datagy.io/python-sha256/

    :param a_string: UTF-8 encode-able string
    :return: SHA-256 hash of input string in hex form
    """
    return hashlib.sha256(a_string.encode('utf-8')).hexdigest()


def password_check(passwd: str) -> int:
    """Enforces a secure password and

    Credits https://www.geeksforgeeks.org/password-validation-in-python/
    Forces user to choose a password from 6-20 characters,
        with characters lowercase, uppercase and numbers and
         at least one special symbol: (@, #, $, %).
    No other characters are allowed.

    :param passwd: A password
    :return: Status code indicating the validity of the password
    """

    if len(passwd) < 6:
        return PASSWORD_TOO_SHORT

    if len(passwd) > 20:
        return PASSWORD_TOO_LONG

    if not any(char.isdigit() for char in passwd):
        return PASSWORD_NO_NUMBERS

    if not any(char.isupper() for char in passwd):
        return PASSWORD_NO_UPPERCASE

    if not any(char.islower() for char in passwd):
        return PASSWORD_NO_LOWERCASE

    if not any(char in SPECIAL_SYM for char in passwd):
        return PASSWORD_NO_SPECIAL_SYMBOLS

    allowed_symbols = (*SPECIAL_SYM, *[*string.ascii_letters], *[*string.digits])
    if not all(char in allowed_symbols for char in passwd):
        return PASSWORD_INVALID_SYMBOLS

    return VALID_PASSWORD


# FIXME parameters are str | object because of sentinel object
def input_check(username: str = SENTINEL, email: str = SENTINEL, password: str = SENTINEL) -> int:
    """Checks the validity of provided credentials.

    Characters must be valid to prevent injection attacks.
    Username and e-mail must abide by a standard format.
        email -> 'ascii@sub.domain'
        username -> 'user9_k.1-2'

    :param username: Username to be validated
    :param email: Email to be validated
    :param password: Password to be validated
    :return: Status code conveying the validity status of the parameters
    """
    if username not in ("", SENTINEL, None):
        # Same as email before the '@'
        name_regex = re.compile(r'([A-Za-z\d]+[.-_])*[A-Za-z\d]+')
        if not re.fullmatch(name_regex, username):
            return INVALID_USERNAME
    if email not in ("", SENTINEL, None):
        # Thanks to https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/
        email_regex = re.compile(r'([A-Za-z\d]+[.-_])*[A-Za-z\d]+@[A-Za-z\d-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(email_regex, email):
            return INVALID_EMAIL
    # Password validation (to prevent sql injection and stuff)
    if password not in ("", SENTINEL, None):
        password_status: int = password_check(password)
        if password_status != VALID_PASSWORD:
            return password_status

    return OK
