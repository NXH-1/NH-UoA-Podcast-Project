import pytest

from flask import session
from tests.conftest import client, auth
import podcast.authentication.services as services
import podcast.adapters.repository as repo


@pytest.fixture
def setup_user(client):
    # Create a user with username 'bobby' before running the test
    with client.session_transaction() as sess:
        services.add_user(user_id=1, username='bobby', password='Test#6^0', repo=repo.repo_instance)


def test_register(client):
    # Check that we retrieve the register page
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'user_id': 1, 'password': 'CarelessWhisper1984'}
    )

    assert response.headers['Location'] == '/authentication/login'  # Checking next page is login


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'The username must be at least 3 characters long.'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Password must be at least 8 characters, have upper case letter,\
            a lower case letter and a digit'),
        ('bobby', 'Test#6^0', b'Your username is already taken'),
))
def test_register_with_invalid_input(client, user_name, password, message, setup_user):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'user_id': 1, 'password': password},
        follow_redirects=True
    )
    assert message in response.data


def test_login(setup_user, client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # login
    response = auth.login()

    # # for debugging purposes
    # print('start')
    # print(response.headers)

    # Check that a successful login generates a redirect to the homepage.
    assert response.status_code == 302
    assert response.headers['Location'] == '/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'bobby'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_name' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data


def test_login_required_to_enter_playlist(client, setup_user, auth):
    status_code = client.get('/playlist').status_code
    # checking that it moves to another location when not logged in
    assert status_code == 302
    response = client.get('/playlist')
    # checking that without login, it will bring user to a login page
    assert response.headers['Location'] == '/authentication/login'


def test_entering_playlist(client, setup_user, auth):
    auth.login()

    response = client.get('/playlist')
    # checks that it retrieves the playlist page when logged in
    assert response.status_code == 200
    assert b'Playlist' in response.data


def test_add_episode_to_playlist(client, setup_user, auth):
    auth.login()

    response = client.get('/add_to_playlist/1')
    # check that it does not relocate to authentication pages
    assert response.headers['Location'] != '/authentication/login'
    print(response.data.decode('utf-8'))

    # Checks that redirects to a description page
    assert b'description' in response.data
    # episode_id 1 is part of podcast_id 14
    assert b'14' in response.data


def test_login_required_to_add_episode_to_playlist(client, setup_user, auth):
    response = client.get('/add_to_playlist/1')
    # checking that it moves to another location when not logged in
    assert response.headers['Location'] == '/authentication/login'


# did not test for remove episode because it cannot be reached without adding episodes

def test_login_required_add_review(client, setup_user, auth):
    response = client.get('/add_review/1')
    # checking that it moves to another location when not logged in
    assert response.headers['Location'] == '/authentication/login'


def test_add_review(client, setup_user, auth):
    auth.login()

    response = client.get('/add_review/1')
    # check that it does not relocate to authentication pages
    print(response.data.decode('utf-8'))
    # shows that it bring user to review page successfully
    assert response.status_code == 200

    # review page title(header)
    assert b'Reviewing...' in response.data
    #  podcast id 1 is D-Hour Radio Network so, it is expected to be reviewing this podcast so should be in the data
    assert b'D-Hour Radio Network' in response.data


@pytest.mark.parametrize(('comment', 'messages'), (
        ('F*** this podcast', (b'Your comment must not contain profanity')),
        ('Hey', (b'Your comment is too short')),
        ('ass', (b'Your comment is too short')),  # stops you from commenting if its too short anyway so no profanity
        # so no profanity warning
        ('you ass', (b'Your comment must not contain profanity'))  # shows that ass is profanity
))
def test_comment_with_invalid_input(client, auth, comment, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on podcast.
    response = client.post(
        '/add_review/1',
        data={'comment': comment, 'rating': '5'}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_searching(client, setup_user, auth):
    response = client.get('/search')
    # Can get to a searched page even if not logged in
    assert response.status_code == 200
    assert b'You searched for:' in response.data
    response = client.post(
        '/search',
        data={'searched': 'Roy Green Show', 'filter': 'title'}
    )
    # Checked that it searched for it
    assert b'Roy Green Show' in response.data

    # Login a user.
    auth.login()

    # Works the same when logged in
    assert response.status_code == 200
    assert b'You searched for:' in response.data
    response = client.post(
        '/search',
        data={'searched': 'Roy Green Show', 'filter': 'title'}
    )
    # Checked that it searched for it
    assert b'Roy Green Show' in response.data


def test_add_all_episodes_to_playlist(client, setup_user, auth):
    auth.login()

    response = client.get('/add_podcast_to_playlist/1')
    # check that it does not relocate to authentication pages
    assert response.headers['Location'] != '/authentication/login'
    print(response.data.decode('utf-8'))

    # Checks that redirects to a description page
    assert b'description' in response.data
    # podcast ID 1 being removed
    assert b'/1?' in response.data


def test_login_required_add_all_episodes_to_playlist(client, setup_user, auth):
    response = client.get('/add_podcast_to_playlist/1')
    # checking that it moves to another location when not logged in
    assert response.headers['Location'] == '/authentication/login'


def test_remove_all_episodes_from_playlist(client, setup_user, auth):
    auth.login()

    response = client.get('/remove_podcast_from_playlist/1')
    # check that it does not relocate to authentication pages
    assert response.headers['Location'] != '/authentication/login'

    # Checks that redirects to a description page
    assert b'description' in response.data
    # podcast ID 1 being removed
    assert b'/1?' in response.data


def test_login_required_remove_all_episodes_from_playlist(client, setup_user, auth):
    response = client.get('/remove_podcast_from_playlist/1')
    # checking that it moves to another location when not logged in
    assert response.headers['Location'] == '/authentication/login'
