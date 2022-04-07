def v1_access_token_post():  # noqa: E501
    """Log-in Step 2 (Tokens) - Give valid authorization code. Return access token if code is valid.

    Authorization code is obtained through a log-in process with &#39;/auth-token&#39;. # noqa: E501

    :rtype: None
    """
    return 'do some magic!'


def v1_auth_token_post():  # noqa: E501
    """Log-in Step 1 (Credentials) - Input valid credentials. Return valid authorization code.

    Parameters are username/e-mail and password. If valid credentials, return valid authorization code, which will be traded at &#39;/access-token&#39; for an access token. # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def v1_signout_post():  # noqa: E501
    """Deletes an user from the registry.

    Deletes an user from the registry. # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def v1_signup_post():  # noqa: E501
    """Registers an user to the database with the given credentials.

    Give the e-mail, username and password as parameters. Registers a new user with those credentials in the userbase. # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def v1_validate_access_token_post():  # noqa: E501
    """Log-in Step 3 (Validation) - Check validity of access token.

    Check if parameter access token is valid. This call is used by other modules to authenticate a user. # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
