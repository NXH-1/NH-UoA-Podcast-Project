from werkzeug.security import generate_password_hash, check_password_hash

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(user_id: int, username: str, password: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is not None:
        raise NameNotUniqueException("The username already exists.")
    hashed_password = generate_password_hash(password)

    new_user = User(user_id, username=username, password=hashed_password)
    print(f"New user: {new_user.password}")
    repo.add_user(new_user)


def authenticate_user(username: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(username)

    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException("The username or password is incorrect.")


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def user_to_dict(user: User):
    user_dict = {
        'username': user.username,
        'password': user.password,
        'user_id': user.id
    }
    return user_dict
