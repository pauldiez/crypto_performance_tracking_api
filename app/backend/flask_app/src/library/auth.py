from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from src.app import Config


def generate_auth_token(expiration=(12 * 2592000)):
    """Generate auth token

    :param expiration: expiration default it set to 1 year
    :return:
    """

    # Create serializer to encrypt our data
    serializer = Serializer(Config.SECRET_KEY, expires_in=expiration)
    token = serializer.dumps({'user_id': "chart_user_01"})

    # Return our token as a string
    return token.decode('ascii')
