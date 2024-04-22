from mcore.models import User, UserCreator, UserPasswordHash
from mcore.errors import MStackAuthenticationError, NotFoundError
from mcore.auth import *
from mcore.util import example_model
from mcore.db import MongoDB

from ..conftest import reset_collection

import pytest

db = MongoDB.from_cache()

def test_user_creator():

    data = {
        'email': 'email@example.com',
        'phone_number': 'tel:+1-513-555-0123',
        'first_name': 'Alice',
        'last_name': 'Smith',
        'middle_name': 'C',
        'password1': 'password',
        'password2': 'password'
    }

    # valid model #
    user_creator = UserCreator(**data)
    assert user_creator.password1 == user_creator.password2

    user = user_creator.create_model()
    assert isinstance(user, User)
    assert getattr(user, 'password1', None) == None
    assert getattr(user, 'password2', None) == None

    user_dumped = user.model_dump()
    assert 'password1' not in user_dumped
    assert 'password2' not in user_dumped

    user_json = user.model_dump_json()
    assert 'password1' not in user_json
    assert 'password2' not in user_json

    # mismatched passwords #

    data['password2'] = 'Password'

    with pytest.raises(ValueError):
        user_creator = UserCreator(**data)

    # short password #

    data['password1'] = 'short'
    data['password2'] = 'short'

    with pytest.raises(ValueError):
        user_creator = UserCreator(**data)


def test_password_verification():
    password = 'here is a very secure password'
    hash = get_password_hash(password)
    assert verify_password(password, hash)
    assert not verify_password('wrong password', hash)


def test_user_create_procedure():
    user_creator:UserCreator = example_model(UserCreator)

    reset_collection(User)
    reset_collection(UserPasswordHash)

    user = create_new_user(user_creator)
    assert user.id is not None
    assert user.cid is not None

    with pytest.raises(MStackAuthenticationError, match='Email already registered'):
        create_new_user(user_creator)

    with pytest.raises(MStackAuthenticationError, match='Invalid username or password'):
        authenticate_user(user.email, 'wrong password')

    authenticate_user(user.email, user_creator.password1)

    delete_user(user)

    with pytest.raises(NotFoundError):
        db.find_one(User, {'email': user.email})
