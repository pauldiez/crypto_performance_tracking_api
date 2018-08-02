from flask import g
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from src.app import api, auth, Config
from src.resources.feed import FeedCollectionResource
from src.resources.auth import AuthResource


@auth.verify_password
def verify_password(username_or_token, password):
    """Verify password

    :param username_or_token:
    :param password:
    :return None, Boolean:
    """

    # Load token serializer
    serializer = Serializer(Config.SECRET_KEY)

    try:

        # First try to authenticate by token
        data = serializer.loads(username_or_token)

    except SignatureExpired:
        return None
    except BadSignature:
        return None

    if "user_id" in data:

        # We don't need this for now - but a reminder to do something
        # with this when time comes.
        if data['user_id'] == 'chart_user_01':
            # g.current_user = data['user_id']
            return True

    return None


# Register api endpoints
api.add_resource(FeedCollectionResource, '/feed/<string:crypto_symbol>',
                 endpoint="api.feeds")
# api.add_resource(AuthResource, '/auth/token', endpoint="api.auth")
