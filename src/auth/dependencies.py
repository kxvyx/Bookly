from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_access_token
from fastapi.exceptions import HTTPException

class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request)->HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token_data = decode_access_token(creds.credentials)

        if token_data is None:
            raise HTTPException(status_code=401, detail="Invalid or expired access token")

        if token_data.get("refresh"):
            raise HTTPException(status_code=401, detail="Please provide an access token, not a refresh token")

        return token_data


    def token_valid(self, token:str)->bool:
        token_data = decode_access_token(token)
        if token_data:
            return True
        return False