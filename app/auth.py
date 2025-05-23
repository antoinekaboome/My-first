import base64
import hashlib
import hmac
import json
import time
from typing import Optional

SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def base64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def jwt_encode(payload: dict, key: str = SECRET_KEY, algorithm: str = ALGORITHM) -> str:
    header = {"alg": algorithm, "typ": "JWT"}
    header_b64 = base64url_encode(json.dumps(header, separators=(',', ':')).encode())
    payload_b64 = base64url_encode(json.dumps(payload, separators=(',', ':')).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(key.encode(), signing_input, hashlib.sha256).digest()
    signature_b64 = base64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def jwt_decode(token: str, key: str = SECRET_KEY, algorithms: Optional[list] = None) -> dict:
    try:
        header_b64, payload_b64, signature_b64 = token.split('.')
        signing_input = f"{header_b64}.{payload_b64}".encode()
        signature = base64url_decode(signature_b64)
        expected_sig = hmac.new(key.encode(), signing_input, hashlib.sha256).digest()
        if not hmac.compare_digest(signature, expected_sig):
            raise ValueError("Invalid signature")
        payload = json.loads(base64url_decode(payload_b64))
        if payload.get('exp') and payload['exp'] < int(time.time()):
            raise ValueError('Token expired')
        return payload
    except Exception as e:
        raise ValueError('Invalid token') from e


def create_access_token(data: dict, expires_delta: int = 3600) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": int(time.time()) + expires_delta})
    return jwt_encode(to_encode)

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def get_current_user_token(token: str = Depends(oauth2_scheme)):
    try:
        return jwt_decode(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")
