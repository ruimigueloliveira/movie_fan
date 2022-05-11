from typing import Dict

SPECIAL_SYM: tuple = ('$', '@', '#', '%')

ERROR: int = -1
OK: int = 0
INVALID_USERNAME: int = 1
INVALID_EMAIL: int = 2
INVALID_PASSWORD: int = 3
NON_EXISTENT_USER: int = 4
USER_ALREADY_EXISTS: int = 5
INVALID_TOKEN: int = 6
VALID_USERNAME: int = 10
VALID_EMAIL: int = 20
VALID_PASSWORD: int = 30
PASSWORD_TOO_SHORT: int = 31
PASSWORD_TOO_LONG: int = 32
PASSWORD_NO_NUMBERS: int = 33
PASSWORD_NO_UPPERCASE: int = 34
PASSWORD_NO_LOWERCASE: int = 35
PASSWORD_NO_SPECIAL_SYMBOLS: int = 36
VALID_CREDENTIALS: int = 40
NON_EXISTENT_USERNAME: int = 41
NON_EXISTENT_EMAIL: int = 42
WRONG_PASSWORD: int = 43
MISMATCH_USERNAME_EMAIL: int = 44
USER_PARAMETERS_AVAILABLE: int = 50
USERNAME_ALREADY_EXISTS: int = 51
EMAIL_ALREADY_EXISTS: int = 52
VALID_TOKEN: int = 60
INVALID_AUTH_CODE: int = 61
INVALID_ACCESS_TOKEN: int = 62
OVERDUE_ACCESS_TOKEN: int = 63


def status_description(code: int) -> str:
    """

    :param code: Status code integer
    :return: Status code description
    """

    # Parameter parse
    code = int(code)

    # Status code list w/ descriptions
    statuses: Dict[int, str] = {
        ERROR: "Operation failed",
        OK: "OK / Operation success",
        INVALID_USERNAME: "Username is not valid",
        INVALID_EMAIL: "Email is not valid",
        INVALID_PASSWORD: "Password is not valid",
        NON_EXISTENT_USER: "User with requested credentials does not exist",
        USER_ALREADY_EXISTS: "Can't add user, he already exists!",
        INVALID_TOKEN: "Invalid token!",
        VALID_USERNAME: "Username is valid",
        VALID_EMAIL: "Email is valid",
        VALID_PASSWORD: "Password is valid",
        PASSWORD_TOO_LONG: "Length should be at least 6",
        PASSWORD_TOO_SHORT: "Length should be not be greater than 8",
        PASSWORD_NO_NUMBERS: "Password should have at least one numeral",
        PASSWORD_NO_UPPERCASE: "Password should have at least one uppercase letter",
        PASSWORD_NO_LOWERCASE: "Password should have at least one lowercase letter",
        PASSWORD_NO_SPECIAL_SYMBOLS: f'Password should have at least one of the symbols {"".join(SPECIAL_SYM)}',
        VALID_CREDENTIALS: "Input credentials are valid",
        NON_EXISTENT_USERNAME: "Username does not exist",
        NON_EXISTENT_EMAIL: "E-mail does not exist",
        WRONG_PASSWORD: "Password incorrect",
        MISMATCH_USERNAME_EMAIL: "Username and e-mail do not match",
        USERNAME_ALREADY_EXISTS: "Username already used!",
        EMAIL_ALREADY_EXISTS: "Email is already in use!",
        INVALID_AUTH_CODE: "Authorization code is invalid!",
        INVALID_ACCESS_TOKEN: "Access token is not valid!",
        OVERDUE_ACCESS_TOKEN: "Access token is no longer valid!",
    }

    # Validate code
    if code not in statuses.keys():
        return f"Invalid status code: {code}!"

    return statuses[code]
