import os

from mcore.db import MongoDB
from mcore.errors import MStackAuthenticationError, NotFoundError
from mcore.models import User, UserCreator, UserPasswordHash, Profile

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
    'delete_profile'
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
        user:User = db.find_one(User, {'email': email.lower()})
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
    user.email = user.email.lower()

    try:
        db.find_one(User, {'email': user.email})
    except NotFoundError:
        """if user not found we can continue creating a user,
        note that this check is not a substitute for a unique index on the email field in the database"""
    else:
        raise MStackAuthenticationError('Email already registered')

    db.create(user)

    user_password_hash = UserPasswordHash(user_id=user.id, hashed_password=get_password_hash(user_creator.password1))
    db.create(user_password_hash)

    return user


def delete_user(user:User) -> None:
    """
    placeholder for a future function that will delete a user and all associated data after a waiting period
    """

    db = MongoDB.from_cache()
    try:
        user_pw:UserPasswordHash = list(db.find(UserPasswordHash, {'user_id': user.id}))[0]
        db.delete(UserPasswordHash, id=user_pw.id)
    except IndexError:
        pass
    
    db.delete(User, id=user.id)


def delete_profile(profile:Profile, logged_in_user:User) -> None:
    """
    placeholder for a future function that will delete a profile and all associated data after a waiting period
    """
    if profile.user_cid != logged_in_user.cid:
        raise MStackAuthenticationError('Only logged in user can delete their own profile')
    
    db = MongoDB.from_cache()
    db.delete(Profile, id=profile.id)
