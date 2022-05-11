from flask import request
from auth_lib import oauth_operations, users_operations, statuses


def v1_auth_token_post():  # noqa: E501
    """Log-in Step 1 (Credentials) - Input valid credentials. Return valid authorization code.

    Parameters are username/e-mail and password. If valid credentials, return valid authorization code, which will be traded at &#39;/access-token&#39; for an access token. # noqa: E501


    :rtype: None
    """
    # Extract parameters
    username, email, password = [request.json.get(param) for param in ("username", "email", "password")]
    # Call auth-lib
    status_code, auth_code = oauth_operations.authorization_code(username, email, password)
    # Return status code
    return dict(
        status_code=str(status_code), status=statuses.status_description(status_code), auth_code=auth_code.hex()
    )


def v1_signup_post():  # noqa: E501
    """Registers an user to the database with the given credentials.

    Give the e-mail, username and password as parameters.
    Registers a new user with those credentials in the userbase. # noqa: E501


    :rtype: None
    """
    # Extract parameters
    username, email, password = [request.json[param] for param in ("username", "email", "password")]
    # Call auth-lib
    status_code: int = users_operations.register(username, email, password)
    # Return status code
    return dict(status_code=str(status_code), status=statuses.status_description(status_code))


def v1_access_token_post():  # noqa: E501
    """Log-in Step 2 (Tokens) - Give valid authorization code. Return access token if code is valid.

    Authorization code is obtained through a log-in process with &#39;/auth-token&#39;. # noqa: E501


    :rtype: None
    """
    # Extract parameters
    auth_code, username, email, password = [
        request.json[param] for param in ("authtoken", "username", "email", "password")
    ]
    # Call auth-lib
    status_code, access_token = oauth_operations.generate_access_token(bytes.fromhex(auth_code), username, email, password)
    # Split, parse and join
    signature, deadline = access_token.split(b"-ds")
    access_token = "-ds".join(
        [signature.hex(), str(deadline, "utf-8")]
    )
    # Return status code
    return dict(
        status_code=status_code,
        status=statuses.status_description(status_code),
        access_token=access_token
    )


def v1_signout_post():  # noqa: E501
    """Deletes an user from the registry.

    Deletes an user from the registry. # noqa: E501


    :rtype: None
    """
    # Extract parameters
    username, email, password = [request.json[param] for param in ("username", "email", "password")]
    # Call auth-lib
    status_code: int = users_operations.remove(password, username, email)
    # Return status code
    return dict(
        status_code=str(status_code),
        status=statuses.status_description(status_code)
    )


def v1_validate_access_token_post():  # noqa: E501
    """Log-in Step 3 (Validation) - Check validity of access token.

    Check if parameter access token is valid. This call is used by other modules to authenticate a user. # noqa: E501


    :rtype: None
    """
    # Extract parameters
    access_token, auth_code = (request.json[param] for param in ("access_token", "auth_code"))
    # Call auth-lib
    status_code = oauth_operations.validate_access_token(
        bytes.fromhex(access_token.split("-ds")[0]) + b"-ds" + bytes(access_token.split('-ds')[1], "utf-8"),
        bytes(auth_code, "utf-8")
    )
    # Return status code
    return dict(status_code=str(status_code), status=statuses.status_description(status_code))
