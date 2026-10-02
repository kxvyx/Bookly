import logging
import uuid
from passlib.context import CryptContext
from datetime import timedelta , datetime
import jwt
from src.config import Config

password_context = CryptContext(
    schemes=['bcrypt']
)

AccessTokenExpiry = 3600

def generate_password_hash(password:str)->str:
    hash = password_context.hash(password)
    return hash

def verify_password(password:str, hash:str)->bool:
    return password_context.verify(password,hash)

def create_access_token(user_data:dict , expiry:timedelta=None, resfresh:bool=False)->str:
    payload = {}
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry else timedelta(seconds=AccessTokenExpiry))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = resfresh

    token = jwt.encode(
        payload = payload,
        key = Config.JWT_SECRET_KEY,
        algorithm = Config.JWT_ALGO
    )

    return token

def decode_access_token(token:str)->dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key = Config.JWT_SECRET_KEY,
            algorithms = [Config.JWT_ALGO]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None