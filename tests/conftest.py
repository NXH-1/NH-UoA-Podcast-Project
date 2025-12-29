import pytest
import os

from podcast import create_app
from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters import repository_populate

test_data_path = os.path.dirname(os.path.abspath(__file__))


# Creates a repository for testing using test csv files
# which is a much smaller size scale
@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    database_mode = False
    repository_populate.populate(test_data_path, repo, database_mode)
    return repo


# phase 2

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,  # Set to True during testing.
        'REPOSITORY': 'memory',
        'TEST_DATA_PATH': test_data_path,  # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False  # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='bobby', password='Test#6^0'):
        return self.__client.post(
            'authentication/login',
            data={'user_name': user_name, 'user_id': 1, 'password': password}
        )

    def logout(self):
        return self.__client.get('/authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
