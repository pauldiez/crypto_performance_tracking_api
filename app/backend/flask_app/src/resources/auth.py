from src.library.auth import generate_auth_token
from flask_restful import Resource


class AuthResource(Resource):

    def get(self):
        """
        Generate auth token

        :return:
        """
        token = generate_auth_token()
        return {"token": token}, 200, {"content-type": "application/json"}
