from langflow.custom import Component
from langflow.inputs import MessageTextInput
from langflow.template import Output
from langflow.schema.message import Message
import jwt
import requests

class JWTValidatorComponent(Component):
    display_name = "JWT Validator"
    description = "Validates a JWT and extracts the user ID."
    icon = "lock"

    inputs = [
        MessageTextInput(
            name="jwt_token",
            display_name="JWT Token",
            required=True,
            info="The JSON Web Token to validate",
        ),
        MessageTextInput(
            name="jwks_url",
            display_name="JWKS URL",
            required=True,
            value="https://test.com/.well-known/jwks.json",
            info="URL of the JSON Web Key Set for token validation",
        ),
    ]
    outputs = [
        Output(display_name="User ID", name="user_id", method="validate_auth"),
    ]

    def validate_auth(self) -> Message:
        response = requests.get(self.jwks_url)
        jwks = response.json()
        headers = jwt.get_unverified_header(self.jwt_token)
        key = next(k for k in jwks["keys"] if k["kid"] == headers["kid"])
        payload = jwt.decode(self.jwt_token, key, algorithms=["RS256"])
        return Message(content=payload["sub"])