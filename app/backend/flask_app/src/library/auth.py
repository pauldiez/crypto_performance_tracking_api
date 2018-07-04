from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from src.app import Config

def generate_auth_token(expiration=(12*2592000)):
    """
    Generate auth token

    :param expiration: expiration default it set to 1 year
    :return:
    """
    serializer = Serializer(Config.SECRET_KEY, expires_in=expiration)
    token = serializer.dumps({'user_id': "chart_user_01"})
    return token.decode('ascii')

