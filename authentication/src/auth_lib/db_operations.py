"""CRUD operations to the users credentials database

"""
from typing import Optional

import pymongo

from auth_lib.statuses import OK, USER_ALREADY_EXISTS, NON_EXISTENT_USER, USERNAME_ALREADY_EXISTS,\
    EMAIL_ALREADY_EXISTS, MISMATCH_USERNAME_EMAIL, WRONG_PASSWORD
from auth_lib.utils import hash_unicode, SENTINEL, input_check

# Constants
AUTH_DB_NAME: str = "auth"
CREDENTIALS_COLLECTION_NAME: str = "creds_list"

# Initialize client mongo container
auth_client = pymongo.MongoClient("auth-mongodb-service", 27017)


def get_user_creds(username: str) -> Optional[dict]:
    """[Read] Get the credentials (SHA-256 hashed) of the user w/ the requested username

    """

    query = dict(username_h=hash_unicode(username))

    return auth_client[AUTH_DB_NAME][CREDENTIALS_COLLECTION_NAME].find_one(query)


def remove(password: str, username: str = SENTINEL, email: str = SENTINEL) -> int:
    """[Delete] Removes a user from the database

    :param password:
    :param username:
    :param email:
    :return: Status code
    """

    # Validate user
    status_: int = check(password, username, email)
    if status_ != OK:
        return status_

    # Remove row from df
    query = dict(username_h=hash_unicode(username))
    auth_client[AUTH_DB_NAME][CREDENTIALS_COLLECTION_NAME].delete_one(query)

    return OK


def _add_db_user(email_h: str, password_h: str, username_h: str) -> int:
    """[Create] Adds a user to the database

    Assumes the credentials' collection is empty

    """

    auth_db = auth_client[AUTH_DB_NAME]
    creds_list = auth_db[CREDENTIALS_COLLECTION_NAME]

    creds_list.insert_one(
        dict(username_h=username_h, email_h=email_h, password_h=password_h)
    )

    return OK


def _email_exists(email_h: str) -> bool:
    query = dict(email_h=email_h)

    return auth_client[AUTH_DB_NAME][CREDENTIALS_COLLECTION_NAME].find_one(query) is not None


def _username_exists(username_h: str):
    query = dict(username_h=username_h)

    return auth_client[AUTH_DB_NAME][CREDENTIALS_COLLECTION_NAME].find_one(query) is not None


def register(username: str, email: str, password: str) -> int:
    """[Create] Registers users data (SHA-256 hashed) to the registry
    :param username: User pseudonym
    :param email: User e-mail
    :param password: User password
    :return: Status code
    """

    # Validate input
    status_: int = input_check(username, email)
    if status_ != OK:
        return status_

    # Hash the parameters
    username_h, email_h, password_h = [hash_unicode(value) for value in (username, email, password)]

    # Check if user exists
    user_presence_check = check(password, username, email)
    if user_presence_check == OK:
        return USER_ALREADY_EXISTS
    assert user_presence_check == NON_EXISTENT_USER, f"Unexpected status at user registration," \
                                                     f" while checking if he is present in db: {user_presence_check}"

    # Check if username or email exist
    if _username_exists(username_h):
        return USERNAME_ALREADY_EXISTS
    if _email_exists(email):
        return EMAIL_ALREADY_EXISTS

    # Append line with hashes to csv
    return _add_db_user(email_h, password_h, username_h)


def check(password: str, username: str, email: Optional[str] = None) -> int:
    """Check if a user with the provided parameters exist

     MUST provide at least either username or email

    :param password: User password
    :param username:
    :param email: Optional* parameter
    :return: Status code
    """
    # Validate input
    status_: int = input_check(username, email, password)
    if status_ != OK:
        return status_

    user_doc: Optional[dict] = get_user_creds(username)

    # If user_row is empty, return some error indicating that the user doesn't exist
    if user_doc is None:
        return NON_EXISTENT_USER

    # Verification: If email is not empty, check if it matches with username
    if email is not None:
        claimed_email: str = hash_unicode(email)

        # Get email associated with username
        actual_email: str = user_doc.get("email_h")
        if actual_email != claimed_email:
            return MISMATCH_USERNAME_EMAIL

    claimed_passwd: str = hash_unicode(password)
    actual_passwd: str = user_doc.get("password_h")

    if claimed_passwd != actual_passwd:
        return WRONG_PASSWORD

    return OK
