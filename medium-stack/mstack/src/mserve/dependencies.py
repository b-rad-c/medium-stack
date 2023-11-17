from mcore.models import User


async def current_user() -> User:
    params = User.model_json_schema()['examples'][0]
    return User(**params)
