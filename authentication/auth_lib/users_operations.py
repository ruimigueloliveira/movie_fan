import hashlib
import os.path
import re
import pandas as pd

# --- Constants ---
# Sentinel design pattern
from auth_lib import statuses
from auth_lib.statuses import OK, INVALID_USERNAME, INVALID_EMAIL, USER_ALREADY_EXISTS, VALID_PASSWORD, \
    PASSWORD_TOO_SHORT, \
    PASSWORD_TOO_LONG, PASSWORD_NO_NUMBERS, PASSWORD_NO_UPPERCASE, PASSWORD_NO_LOWERCASE, PASSWORD_NO_SPECIAL_SYMBOLS, \
    WRONG_PASSWORD, MISMATCH_USERNAME_EMAIL, USERNAME_ALREADY_EXISTS, EMAIL_ALREADY_EXISTS, SPECIAL_SYM, \
    NON_EXISTENT_USER

SENTINEL = object()
# Status codes
# Misc
USERS_DB: str = f"{os.path.dirname(__file__)}/users.csv"


def hash_unicode(a_string: str) -> str:
    """
    Reference: https://datagy.io/python-sha256/
    :param a_string: UTF-8 encode-able string
    :return: SHA-256 hash of input string in hex form
    """
    return hashlib.sha256(a_string.encode('utf-8')).hexdigest()


def password_check(passwd: str) -> int:
    """
    Credits https://www.geeksforgeeks.org/password-validation-in-python/
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

    return VALID_PASSWORD


# FIXME parameters are str | object because of sentinel object
def input_check(username: str = SENTINEL, email: str = SENTINEL, password: str = SENTINEL) -> int:
    """

    :param username: Username to be validated
    :param email: Email to be validated
    :param password: Password to be validated
    :return: Status code conveying the validity status of the parameters
    """
    if username != "" and username is not SENTINEL:
        # Same as email before the '@'
        name_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+')
        if not re.fullmatch(name_regex, username):
            return INVALID_USERNAME
    if email != "" and email is not SENTINEL:
        # Thanks to https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(email_regex, email):
            return INVALID_EMAIL
    # Password validation (to prevent sql injection and stuff)
    if password != "" and password is not SENTINEL:
        password_status: int = password_check(password)
        if password_status != VALID_PASSWORD:
            return password_status

    return OK


def register(username: str, email: str, password: str) -> int:
    """
    Registers users data (SHA-256 hashed) to the registry at users.csv
    :param username: User pseudonym
    :param email: User e-mail
    :param password: User password
    :return: Status code
    """

    # Validate input
    status: int = input_check(username, email)
    if status != OK:
        return status

    # Hash the parameters
    username_h, email_h, password_h = [hash_unicode(value) for value in (username, email, password)]

    # Write to the csv
    no_file: bool = not os.path.exists(USERS_DB)
    if no_file:
        # Create the file and write the headers
        with open(USERS_DB, 'w') as nf:
            nf.write("username,email,password\n"
                     f"{username_h},{email_h},{password_h}")
        return OK

    # Check if user exists
    user_presence_check = check(password, username, email)
    if user_presence_check == OK:
        return USER_ALREADY_EXISTS
    assert user_presence_check == NON_EXISTENT_USER, f"Unexpected status at user registration," \
                                                     f" while checking if he is present in db: {user_presence_check}"

    # Check if username or email exists
    df = pd.read_csv(USERS_DB)
    if df["username"].str.contains(username_h).sum() > 0:
        return USERNAME_ALREADY_EXISTS
    if df["email"].str.contains(hash_unicode(email)).sum() > 0:
        return EMAIL_ALREADY_EXISTS

    # Append line with hashes to csv
    with open(USERS_DB, 'a') as fd:
        fd.write(f"\n{username_h},{email_h},{password_h}")

    return OK


def check(password: str, username: str, email: str = SENTINEL) -> int:  # or bool?
    """
    Check if a user with the provided parameters exist - must provide at least either username or email
    :param password: User password
    :param username: Optional parameter
    :param email: Optional parameter
    :return: Status code
    """
    # Validate input
    status: int = input_check(username, email, password)
    if status != OK:
        return status

    # Read csv db
    user_db: pd.DataFrame = pd.read_csv(USERS_DB)

    # Search for the user in the registry with the defined password ('s SHA-256)
    #   and obtain the username and email ('s SHA-256)

    # Parse username to hash
    username_h: str = hash_unicode(username)

    # Get user info
    user_row = user_db.loc[user_db['username'] == username_h]

    # If user_row is empty, return some error indicating that the user doesn't exist
    if user_row.empty:
        return NON_EXISTENT_USER

    # Verification: If email is not empty, check if it matches with username
    if email is not SENTINEL:
        claimed_email: str = hash_unicode(email)

        # Get email associated with username
        actual_email: str = user_row["email"].loc[user_row.index[0]]
        if actual_email != claimed_email:
            return MISMATCH_USERNAME_EMAIL

    claimed_passwd: str = hash_unicode(password)
    actual_passwd: str = user_row["password"].loc[user_row.index[0]]

    if claimed_passwd != actual_passwd:
        return WRONG_PASSWORD

    return OK


def remove(password: str, username: str = SENTINEL, email: str = SENTINEL) -> int:
    """

    :param password:
    :param username:
    :param email:
    :return:
    """

    # Validate user
    status: int = check(password, username, email)
    if status != OK:
        return status

    # Read into DataFrame
    df: pd.DataFrame = pd.read_csv(USERS_DB)

    # Remove row from df
    user_row_index = df.loc[df['username'] == hash_unicode(username)].index.to_numpy()[0]
    df = df.drop(index=user_row_index)

    # Write df to csv
    if df.empty:
        # Delete file when it has no data (designer's choice)
        os.remove(USERS_DB)
    else:
        # Just drop the row
        df.to_csv(USERS_DB)

    return OK


if __name__ == '__main__':

    # Register user
    status: int = register(username="andre2", email="andre2@gmail.com", password="andre$P1")
    assert status in (OK, USER_ALREADY_EXISTS), f"Error status: {status}: {statuses.status_description(status)}"

    # Check credentials
    status = check(username="andre2", email="andre2@gmail.com", password="andre$P1")
    assert status == OK, f"Error status: {status}: {statuses.status_description(status)}"

    # Delete user
    status = remove(username="andre2", password="andre$P1")
    assert status == OK, f"Error status: {status}: {statuses.status_description(status)}"
