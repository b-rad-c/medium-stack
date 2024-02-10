import os

from mcore.db import MongoDB
from mcore.errors import MStackAuthenticationError
from mcore.models import User, UserCreator, UserPasswordHash
from mart.models import Artist, ArtistCid

from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

__all__ = [
    'verify_password',
    'get_password_hash',
    'authenticate_user',
    'create_access_token',
    'create_new_user',
    'delete_user',
    'delete_artist'
]


MSTACK_AUTH_SECRET_KEY = os.environ.get('MSTACK_AUTH_SECRET_KEY')   # openssl rand -hex 32
MSTACK_AUTH_ALGORITHM = os.environ.get('MSTACK_AUTH_ALGORITHM', 'HS256')
MSTACK_AUTH_LOGIN_EXPIRATION_MINUTES = os.environ.get('MSTACK_AUTH_LOGIN_EXPIRATION_MINUTES', 60 * 24 * 7)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str) -> User:
    db = MongoDB.from_cache()

    try:
        user:User = list(db.find(User, {'email': email}))[0]
    except IndexError:
        raise MStackAuthenticationError('Invalid username or password (a)')
    
    try:
        user_pw:UserPasswordHash = list(db.find(UserPasswordHash, {'user_id': user.id}))[0]
    except IndexError:
        raise MStackAuthenticationError('Invalid username or password (b)')

    if not verify_password(password, user_pw.hashed_password):
        raise MStackAuthenticationError('Invalid username or password (c)')
    
    return user


def create_access_token(data: dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=MSTACK_AUTH_LOGIN_EXPIRATION_MINUTES)

    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, MSTACK_AUTH_SECRET_KEY, algorithm=MSTACK_AUTH_ALGORITHM)


def create_new_user(user_creator:UserCreator) -> User:
    db = MongoDB.from_cache()

    user = user_creator.create_model()
    db.create(user)

    user_password_hash = UserPasswordHash(user_id=user.id, hashed_password=get_password_hash(user_creator.password1))
    db.create(user_password_hash)

    return user


def delete_user(user:User) -> None:
    """
    placeholder for a future function that will delete a user and all associated data after a waiting period
    """
    db = MongoDB.from_cache()
    db.delete(UserPasswordHash, user_id=user.id)
    db.delete(User, id=user.id)

 
def delete_artist(cid:ArtistCid) -> None:
    """
    placeholder for a future function that will delete an artist and all associated data after a waiting period
    """
    db = MongoDB.from_cache()
    db.delete(Artist, cid=cid)
