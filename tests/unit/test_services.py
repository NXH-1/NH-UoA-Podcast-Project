from datetime import datetime

import pytest

from podcast import User
from podcast.domainmodel.model import Author, Podcast, Review
from tests.conftest import in_memory_repo
from podcast.podcasts.services import (get_podcasts_by_alphabet, get_list_of_podcasts_titles,
                                       NonExistentPodcastException)
from podcast.description.services import (get_episodes, get_podcast_by_id, episodes_to_dict, NonExistentEpisode,
                                          podcast_to_dict, NonExistentPodcast)
from podcast.home.services import (get_random_podcasts, NonExistentPodcastException)

from podcast.authentication import services as auth_services
from podcast.playlist import services as playlist_services
from podcast.description import services as description_services
from podcast.search import services as search_services

from podcast.search.services import pagination


# podcast.services

# Tests whether you can get the podcasts in alphabetical order
def test_get_podcasts_by_alphabet(in_memory_repo):
    titles = get_list_of_podcasts_titles(in_memory_repo)
    sorted_podcasts_dict = get_podcasts_by_alphabet(titles, in_memory_repo)
    # 11 podcast in test csv
    assert len(sorted_podcasts_dict) == len(titles)  # Checks whether the final results still contain the same amount
    assert sorted_podcasts_dict[0]['title'] == "AHDB"  # checks if the first podcast is correct and -
    assert sorted_podcasts_dict[0]['id'] == 100  # if the details are correct
    assert sorted_podcasts_dict[1]['title'] == "Bethel Presbyterian Church (EPC) Sermons"  # A second check on order
    assert sorted_podcasts_dict[1]['id'] == 5  # Checking for second podcast


# Tests whether you can get a list of podcasts titles
def test_get_list_of_podcasts_titles(in_memory_repo):
    list_of_titles = get_list_of_podcasts_titles(in_memory_repo)

    # should be a list of titles from the test csv
    assert list_of_titles == ['D-Hour Radio Network',
                              'Brian Denny Radio',
                              'Onde Road - Radio Popolare',
                              'Tallin Messages',
                              'Bethel Presbyterian Church (EPC) Sermons',
                              'Mike Safo',
                              'The Mandarian Orange Show',
                              'Crawlspace: True Crime & Mysteries',
                              'AHDB',
                              'Locked on Cubs',
                              'Montvale Evangelical Free Church Podcast']
    assert len(list_of_titles) == 11


# description.service
def test_get_episodes(in_memory_repo):
    # podcast id 1 belongs to 'D-Hour Radio Network'
    episodes = get_episodes(1, in_memory_repo)

    # 3 episodes in test csv
    assert len(episodes) == 3
    assert episodes[0].id == 4885
    assert episodes[1].id == 4922
    assert episodes[2].id == 4954

    ep1_date = datetime.strptime(episodes[0].pub_date + '00',
                                 '%Y-%m-%d %H:%M:%S%z')
    ep2_date = datetime.strptime(episodes[1].pub_date + '00',
                                 '%Y-%m-%d %H:%M:%S%z')
    ep3_date = datetime.strptime(episodes[2].pub_date + '00',
                                 '%Y-%m-%d %H:%M:%S%z')
    assert ep1_date < ep2_date
    assert ep2_date < ep3_date


def test_get_podcast_by_id(in_memory_repo):
    podcast_dict1 = get_podcast_by_id(1, in_memory_repo)
    podcast_dict2 = get_podcast_by_id(6, in_memory_repo)

    assert podcast_dict1['id'] == 1
    assert podcast_dict1['title'] == "D-Hour Radio Network"
    assert podcast_dict2['id'] == 6
    assert podcast_dict2['title'] == "Mike Safo"


def test_get_podcast_by_id_raises_exception_when_None(in_memory_repo):
    with pytest.raises(NonExistentPodcast):
        podcast_dict3 = get_podcast_by_id(100, in_memory_repo)


def test_episodes_to_dict(in_memory_repo):
    episode = get_episodes(1, in_memory_repo)
    episode1 = episodes_to_dict(episode)
    assert episode1[0] == {'description': "Say It! Radio is ultimately the people's radio where we talk "
                                          "about hot topics from what's in the news, on the gossip "
                                          "blogs, sports, relationships, love, sex, what's on our "
                                          'listeners mind or whatever...just get it off your chest and '
                                          'Say It! We may agree, disagree, agree, to disagree, but the '
                                          'goal is to learn something new about yourself, own things\xa0'
                                          'about yourself ....learn things about others, see things from '
                                          "different perspective... Low Key....we're going to plant "
                                          'seeds that promote growth.... Shhhhh',
                           'id': 4885,
                           'length': 5280,
                           'link': 'http://www.blogtalkradio.com/dhourshow/2017/12/02/say-it-radio.mp3',
                           'podcast_id': 1,
                           'pub_date': '2017-12-02 02:00:00+00',
                           'title': 'Say It! Radio'}
    assert len(episode1) == 3
    assert type(episode1[0]) == dict
    assert type(episode1[1]) == dict
    assert episode1[1]['title'] == "Say It! Radio"
    assert episode1[2]['title'] == "Say It! Radio...Alter Ego Friday"


# home.services
def test_get_random_podcasts(in_memory_repo):
    podcasts = get_random_podcasts(in_memory_repo)
    podcast_title = podcasts[0]['title']
    sorted_podcasts = get_podcasts_by_alphabet(podcast_title, in_memory_repo)
    # Check that it is title in podcasts
    assert any(podcast['title'] == podcast_title for podcast in sorted_podcasts)
    # Method limits the podcasts size to 10
    assert len(podcasts) == 10
    # creates list of dicts like others
    assert type(podcasts[0]) == dict  # Checking correct type
    assert type(podcasts) == list


# PHASE 2 Testing

# testing if authentication can add users
def test_add_users(in_memory_repo):
    new_user_id = 4420227291029499
    new_user_name = 'name'
    new_password = 'abcd1A23'
    # Created user info to be added
    auth_services.add_user(new_user_id, new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    # checking that user has been added
    assert user_as_dict['username'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('scrypt:32768:8')


# testing not a unique user exception
def test_cannot_add_user_with_existing_name(in_memory_repo):
    new_user_id = 4420227291029499
    new_user_name = 'name'
    new_password = 'abcd1A23'
    # initialise user info
    auth_services.add_user(new_user_id, new_user_name, new_password, in_memory_repo)
    # when attempted to add the user again, the error will occur
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(new_user_id, new_user_name, new_password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_id = 4420227291029499
    new_user_name = 'name'
    new_password = 'abcd1A23'
    # initialise user info
    auth_services.add_user(new_user_id, new_user_name, new_password, in_memory_repo)
    # Authenticate user with correct credentials which will not provoke an error
    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except auth_services.AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_id = 4420227291029499
    new_user_name = 'name'
    new_password = 'abcd1A23'
    # initialise user info
    auth_services.add_user(new_user_id, new_user_name, new_password, in_memory_repo)
    # Check that when the password is wrong the authentication will raise exception
    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


# Testing retrieval of user's playlist
def test_get_user_playlists(in_memory_repo):
    new_user_id = 4420227291029499
    new_user_name = 'name'
    new_password = 'abcd1A23'
    # initialise user info
    auth_services.add_user(new_user_id, new_user_name, new_password, in_memory_repo)
    # Use username to get playlist with the method
    playlist = playlist_services.get_user_playlist(new_user_name, in_memory_repo)
    # checks playlist is by the right user
    assert playlist.user.id == new_user_id
    # Since user has no playlist should make a new empty playlist
    assert playlist.list_of_episodes == []


def test_get_episode_by_id(in_memory_repo):
    episode_id = 1
    # initialised with necessary info
    episode = playlist_services.get_episode_by_id(episode_id, in_memory_repo)
    # checking that id is the same as initialised
    assert episode.id == episode_id
    # checking it has correct info(title) seen in the test episode csv
    assert episode.title == "The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3"


def test_add_episode_to_playlist(in_memory_repo):
    episode_id = 1
    # initialised with necessary info
    episode = playlist_services.get_episode_by_id(episode_id, in_memory_repo)

    new_user_id = 4420227291029499
    new_user_name = 'name'
    new_password = 'abcd1A23'
    # initialise user info
    auth_services.add_user(new_user_id, new_user_name, new_password, in_memory_repo)
    # create playlist for episode to be added
    playlist = playlist_services.get_user_playlist(new_user_name, in_memory_repo)
    assert playlist.list_of_episodes == []
    description_services.add_episode_to_playlist(playlist, episode, in_memory_repo)
    assert playlist.user.id == new_user_id
    assert playlist.list_of_episodes == [episode]  # checking that episode is in playlist after adding
    assert playlist.list_of_episodes[
               0].title == "The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3"


def test_remove_episode_from_playlist(in_memory_repo):
    episode_id = 5
    # initialised with necessary info
    episode2 = playlist_services.get_episode_by_id(episode_id, in_memory_repo)
    new_user_id = 4420227291029499
    new_user_name = 'name'
    new_password = 'abcd1A23'
    # initialise user info
    auth_services.add_user(new_user_id, new_user_name, new_password, in_memory_repo)
    # create playlist for episode to be added
    playlist = playlist_services.get_user_playlist(new_user_name, in_memory_repo)
    assert playlist.list_of_episodes == []
    description_services.add_episode_to_playlist(playlist, episode2, in_memory_repo)
    assert playlist.list_of_episodes == [episode2]
    assert playlist.list_of_episodes[0].pod_id == 14  # Check that info of episode is correct
    assert playlist.list_of_episodes[
               0].title == "The Mandarian Orange Show Episode 75- The Luggage Gamble, or: 30 Day MoviePass Challenge Part 4"

    description_services.remove_episode_from_playlist(playlist, episode2, in_memory_repo)
    assert playlist.list_of_episodes == []  # check that the episode has been removed after use of the method


def test_get_episode_podcast_dict(in_memory_repo):
    podcast1 = in_memory_repo.get_podcast(1)  # D-Hour Radio Network
    podcast2 = in_memory_repo.get_podcast(177)  # Locked on Cubs

    # initialise some episodes for the list
    episode1 = playlist_services.get_episode_by_id(11, in_memory_repo)  # Locked on Cubs
    episode2 = playlist_services.get_episode_by_id(12, in_memory_repo)  # Locked on Cubs
    episode3 = playlist_services.get_episode_by_id(13, in_memory_repo)  # Locked on Cubs
    episode4 = playlist_services.get_episode_by_id(15, in_memory_repo)  # D-Hour Radio Network
    episode5 = playlist_services.get_episode_by_id(18, in_memory_repo)  # D-Hour Radio Network
    episode6 = playlist_services.get_episode_by_id(19, in_memory_repo)  # D-Hour Radio Network

    episode_list = [episode1, episode2, episode3, episode4, episode5, episode6]

    # use method to get the dict
    ep_pod_dict = playlist_services.episode_podcast_dict(episode_list, in_memory_repo)

    # get an episode from the list to check
    assert ep_pod_dict[episode1] == podcast2  # check that the episode added in first is corresponding
    assert ep_pod_dict[episode1].title == podcast2.title  # to the correct podcast
    assert ep_pod_dict[episode1].description == podcast2.description
    # check the rest of the episodes is correctly matched up with podcast
    assert ep_pod_dict[episode2] == podcast2
    assert ep_pod_dict[episode3] == podcast2
    assert ep_pod_dict[episode4] == podcast1
    assert ep_pod_dict[episode5] == podcast1
    assert ep_pod_dict[episode6] == podcast1


def test_add_review_to_podcast(in_memory_repo):
    user = User(1, "test_user", "password")
    author = Author(1111, "teeeeeeeest")
    podcast = Podcast(101, author, "Test Podcast", "image_url", "Description", "website", 111111, "English")

    in_memory_repo.add_user(user)
    in_memory_repo.add_podcast(podcast)

    # call
    description_services.add_review_to_podcast("test_user", 101, "Great podcast!", 5, in_memory_repo)

    # check
    reviews = in_memory_repo.get_reviews_for_podcast(101)
    assert len(reviews) == 1
    assert reviews[0]._content == "Great podcast!"
    assert reviews[0]._rating == 5
    assert reviews[0].reviewer == user
    assert reviews[0]._podcast == podcast


def test_add_review_to_podcast_raises_exception_for_nonexistent_podcast(in_memory_repo):
    user = User(222, "test_user", "password")
    in_memory_repo.add_user(user)

    # call , should be error
    with pytest.raises(description_services.NonExistentPodcast):
        description_services.add_review_to_podcast("test_user", 999, "Great podcast!", 5, in_memory_repo)


def test_add_review_to_podcast_raises_exception_for_unknown_user(in_memory_repo):
    author = Author(123, "Aaaaaaa")
    podcast = Podcast(101, author, "Test Podcast", "image_url", "Description", "website", 111111, "English")
    in_memory_repo.add_podcast(podcast)

    # call , should be error
    with pytest.raises(description_services.UnknownUserException):
        description_services.add_review_to_podcast("unknown_user", 101, "Great podcast!", 5, in_memory_repo)


def test_retrieve_podcast_reviews(in_memory_repo):
    user = User(1, "test_user", "password")
    author = Author(444, "Uuuuuu")
    podcast = Podcast(101, author, "Test Podcast", "image_url", "Description", "website", 111111, "English")
    review = Review(1, user, podcast, 5, "Amazing podcast!")

    in_memory_repo.add_user(user)
    in_memory_repo.add_podcast(podcast)
    in_memory_repo.add_review(review)

    # call
    reviews = description_services.retrieve_podcast_reviews(101, in_memory_repo)

    # check
    assert len(reviews) == 1
    assert reviews[0] == review


def test_retrieve_podcast_reviews_returns_empty_list_when_no_reviews(in_memory_repo):
    author = Author(132, "Ddddd")
    podcast = Podcast(101, author, "Test Podcast", "image_url", "Description", "website", 111111, "English")
    in_memory_repo.add_podcast(podcast)

    # call
    reviews = description_services.retrieve_podcast_reviews(101, in_memory_repo)
    assert len(reviews) == 0


def test_sort_search(in_memory_repo):
    podcasts = in_memory_repo.get_podcasts()

    # Checking that it is currently in Ascending order of IDs
    previous_id = None
    for podcast in podcasts:
        if previous_id is not None:
            assert podcast.id >= previous_id
        previous_id = podcast.id

    # Sorting the podcasts with the method
    sorted_podcasts = search_services.sort_search(podcasts)
    # showing that it is different order
    assert len(sorted_podcasts) == len(podcasts)
    assert podcasts != sorted_podcasts

    # Checking that it is alphabetically sorted
    previous_title = None
    for podcast in sorted_podcasts:
        if previous_title is not None:
            assert podcast.title >= previous_title
        previous_title = podcast.title


def test_pagination():
    # Create a list of 20 sample podcasts
    podcasts = [Podcast(podcast_id=i, title=f"Podcast {i}", author=None) for i in range(1, 21)]

    # Test first page
    page = 1
    paginated_podcasts, total_pages = pagination(page, podcasts)
    assert len(paginated_podcasts) == 8  # First page should contain 8 podcasts.
    assert paginated_podcasts[0]._title == "Podcast 1"  # First podcast on the first page should be 'Podcast 1'.
    assert paginated_podcasts[-1]._title == "Podcast 8"  # Last podcast on the first page should be 'Podcast 8'.
    assert total_pages == 3  # Total pages should be 3.

    # Test second page
    page = 2
    paginated_podcasts, total_pages = pagination(page, podcasts)
    assert len(paginated_podcasts) == 8  # Second page should contain 8 podcasts.
    assert paginated_podcasts[0]._title == "Podcast 9"  # First podcast on the second page should be 'Podcast 9'.
    assert paginated_podcasts[-1]._title == "Podcast 16"  # Last podcast on the second page should be 'Podcast 16'.
    assert total_pages == 3, "Total pages should be 3."

    # Test third page
    page = 3
    paginated_podcasts, total_pages = pagination(page, podcasts)
    assert len(paginated_podcasts) == 4  # Third page should contain 4 podcasts."
    assert paginated_podcasts[0]._title == "Podcast 17"  # First podcast on the third page should be 'Podcast 17'.
    assert paginated_podcasts[-1]._title == "Podcast 20"  # Last podcast on the third page should be 'Podcast 20'.
    assert total_pages == 3, "Total pages should be 3."

    # Test out of range page
    page = 4
    paginated_podcasts, total_pages = pagination(page, podcasts)
    assert len(paginated_podcasts) == 0  # Fourth page should contain no podcasts.
    assert total_pages == 3  # Total pages should be 3.


def test_add_all_episodes_to_playlist(in_memory_repo):
    new_user_id = 4420227291029499
    new_user_name = 'name'
    new_password = 'abcd1A23'
    # initialise user info
    auth_services.add_user(new_user_id, new_user_name, new_password, in_memory_repo)
    # create playlist for episode to be added
    playlist = playlist_services.get_user_playlist(new_user_name, in_memory_repo)

    # Call the function
    description_services.add_all_episodes_to_playlist(playlist, 1, in_memory_repo)

    # Assert that episodes were added to the playlist
    assert len(playlist.list_of_episodes) > 0
    for episode in playlist.list_of_episodes:
        assert episode in in_memory_repo.get_episodes_for_podcast(1)


def test_remove_all_episodes_from_playlist(in_memory_repo):
    new_user_id = 4420227291029499
    new_user_name = 'name'
    new_password = 'abcd1A23'
    # initialise user info
    auth_services.add_user(new_user_id, new_user_name, new_password, in_memory_repo)
    # create playlist for episode to be added
    playlist = playlist_services.get_user_playlist(new_user_name, in_memory_repo)
    episodes = in_memory_repo.get_episodes_for_podcast(1)
    for episode in episodes:
        playlist.add_episode(episode)

    # Call the function
    description_services.remove_all_episodes_from_playlist(playlist, 1, in_memory_repo)

    # Assert that episodes were removed from the playlist
    assert len(playlist.list_of_episodes) == 0
