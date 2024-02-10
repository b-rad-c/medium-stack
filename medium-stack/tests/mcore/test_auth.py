from mcore.models import User, UserCreator
from mcore.auth import *

import pytest


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