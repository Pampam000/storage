from datetime import (
    timedelta,
    datetime
)
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import (
    JWTError,
    jwt
)
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette import status
from storage import settings
from storage.schemas import product as p
from storage.schemas import user as u
from storage.schemas import token as t
from storage.database import tables
from sqlalchemy.orm import Session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_current_user(token: str = Depends(oauth2_scheme)) -> u.User:
    return verify_token(token)


def verify_token(token: str) -> u.User:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.ALGORITHM,
        )
    except JWTError:
        raise exception from None

    user_data = payload.get('user')

    try:
        user = u.User.parse_obj(user_data)
    except ValidationError:
        raise exception from None

    return user


def create_token(user: tables.User) -> t.Token:
    user_data = u.User.from_orm(user)
    now = datetime.utcnow()
    payload = {
        'iat': now,
        'nbf': now,
        'exp': now + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS),

        'user': user_data.dict(),
    }
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return t.Token(access_token=token)


def register_new_user(
        user_data: u.UserCreate,
        db: Session
) -> t.Token:
    gt_us = get_user_by_login(db, user_data.login)
    if gt_us:
        raise HTTPException(
            status_code=405,
            detail='USERNAME HAS ALREADY TAKEN',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    user = tables.User(
        login=user_data.login,
        is_seller=user_data.is_seller,
        hashed_password=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    return create_token(user)


def authenticate_user(
        login: str,
        password: str,
        db: Session
) -> t.Token:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    user = (
        db
        .query(tables.User)
        .filter(tables.User.login == login)
        .first()
    )

    if not user:
        raise exception

    if not verify_password(password, user.hashed_password):
        raise exception

    return create_token(user)


def get_user_by_login(db: Session, login: str):

    return db.query(tables.User).filter(tables.User.login == login).first()
