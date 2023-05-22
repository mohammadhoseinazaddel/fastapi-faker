from datetime import datetime
from typing import List, Optional

from fastapi import status, HTTPException
from fastapi import Depends
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from pydantic import BaseModel, ValidationError
from jose import JWTError, jwt

from system.base.mixins import InterfaceLifeCycle
from system.config import settings
from user.exceptions.auth import InvalidCredential

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/user/login",
)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    scopes: List[str] = []
    expire_at: datetime = None


class JwtInterface(InterfaceLifeCycle):
    def __init__(self, ):
        from fastapi.security import OAuth2PasswordBearer
        from passlib.context import CryptContext

        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def generate_token(
            given_id: int,
            scopes: List[str],
            expire_at: datetime,
            secret_key: str,
            algorithm: str
    ):
        dict_to_encode = {
            "sub": str(given_id),
            "scopes": scopes,
            "exp": expire_at
        }

        return jwt.encode(dict_to_encode, secret_key, algorithm=algorithm)

    # @staticmethod
    # async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    #     try:
    #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    #         user_id: str = payload.get("sub")
    #         if id is None:
    #             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    #
    #         token_scopes = payload.get("scopes", [])
    #         token_data = TokenData(scopes=token_scopes, username=user_id)
    #     except (JWTError, ValidationError):
    #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    #
    #     for scope in security_scopes.scopes:
    #         if scope not in token_data.scopes:
    #             raise HTTPException(
    #                 status_code=status.HTTP_401_UNAUTHORIZED,
    #                 detail="Not Enough Permission"
    #             )
    #     return int(user_id)

    @staticmethod
    def decrypt_token(
            secret_key: str,
            algorithm: str,
            token: str = Depends(oauth2_scheme),
    ):
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            included_id: str = payload.get("sub")
            if included_id is None:
                raise InvalidCredential

            return TokenData(
                id=int(included_id),
                scopes=payload.get("scopes", []),
                expire_at=payload.get("exp")
            )

        except (JWTError, ValidationError):
            raise InvalidCredential


jwt_agent = JwtInterface()
