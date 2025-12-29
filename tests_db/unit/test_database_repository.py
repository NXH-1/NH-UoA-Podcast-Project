import pytest

from podcast.domainmodel.model import Author, Podcast, Category, User, Episode, Review, Playlist
from podcast.adapters.database_repository import SqlAlchemyRepository

from tests_db.conftest import session_factory


def test_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(1, 'Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User(2, 'Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user      # Check that the user Dave got added correctly


def test_can_retrieve_podcast_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_podcasts = repo.get_number_of_podcasts()
    assert number_of_podcasts == 11   # Check that the query returned 11 podcast


def test_get_podcasts(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    # Add an author since Podcast requires an author
    author = Author(author_id=1, name="Test Author")
    repo.add_author(author)

    # Add some podcasts to the database with the required podcast_id
    podcast1 = Podcast(podcast_id=1, title="Podcast 1", author=author)
    podcast2 = Podcast(podcast_id=2, title="Podcast 2", author=author)
    podcast3 = Podcast(podcast_id=12, title="Podcast 3", author=author)
    repo.add_podcast(podcast1)
    repo.add_podcast(podcast2)
    repo.add_podcast(podcast3)


    # Test that get_podcasts returns all podcasts
    podcasts = repo.get_podcasts()
    # Assert: Ensure the length of returned podcasts matches what was added
    assert len(podcasts) == 12    # 12 podcast as we merge 2 since we already have ID 1 and 2 but we add in ID 12

    # Assert: Ensure that the correct podcasts are returned
    assert podcasts[0]._title == "Podcast 1"  # First podcast title should be 'Podcast 1'
    assert podcasts[1]._title == "Podcast 2"  # Second podcast title should be 'Podcast 2'


def test_get_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Fetch the podcast by ID
    fetched_podcast = repo.get_podcast(1)

    # Assert: Check if the correct podcast is fetched
    assert fetched_podcast is not None, "The podcast with ID 1 should be found."
    assert fetched_podcast._title == "D-Hour Radio Network", "This is the Podcast in CSV file"

    # Test for non-existent podcast
    non_existent_podcast = repo.get_podcast(12)
    assert non_existent_podcast is None, "A non-existent podcast should return None."


def test_add_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Check that current is what we see in CSV
    current_podcast = repo.get_podcast(1)
    assert current_podcast._title == "D-Hour Radio Network"
    # Add an author and a podcast
    author = Author(author_id=1, name="Test Author")
    repo.add_author(author)

    podcast = Podcast(podcast_id=1, title="New Podcast", author=author)
    repo.add_podcast(podcast)

    # Fetch all podcasts and ensure the new one is added
    podcast1 = repo.get_podcast(1)

    # Assert: Ensure the new podcast was added correctly
    assert repo.get_number_of_podcasts() == 11  # Remained same as ID 1 already existed
    assert podcast1._title == "New Podcast"  # The added podcast should have the title 'New Podcast'.

    podcast = Podcast(podcast_id=1001, title="Another Podcast", author=author)
    repo.add_podcast(podcast)
    podcast2 = repo.get_podcast(1001)
    assert repo.get_number_of_podcasts() == 12  # Now 12 as podcast with new ID got added
    assert podcast2._title == "Another Podcast"  # The added podcast should have the title 'Another Podcast'.


def test_get_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Add some authors
    author1 = Author(author_id=1, name="Author 1")
    author2 = Author(author_id=10, name="Author 2")
    repo.add_author(author1)
    repo.add_author(author2)

    # Fetch all authors
    authors = repo.get_authors()

    # Assert: Ensure the correct number of authors is returned
    assert len(authors) == 10  # There should be 10 authors. One got added, one got merged
    assert authors[0]._name == "Author 1"  # First author should be 'Author 1'.
    assert authors[9]._name == "Author 2"  # Second author should be 'Author 2'.


def test_add_multiple_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Create a list of authors
    authors_to_add = [Author(author_id=10, name="Author A"), Author(author_id=11, name="Author B")]

    # Add multiple authors
    repo.add_multiple_authors(authors_to_add)

    # Fetch all authors
    authors = repo.get_authors()

    # Assert: Check that the authors were added correctly
    assert len(authors) == 11  # 955 total authors, Two authors should be added.
    assert authors[9]._name == "Author A", "First author should be 'Author A'."
    assert authors[10]._name == "Author B", "Second author should be 'Author B'."


def test_get_reviews_for_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Get podcast from repo
    podcast = repo.get_podcast(1)

    # Add user for Review
    user = User(user_id=1, username="testuser", password="hashedpassword")
    repo.add_user(user)

    # User made review
    review = Review(review_id=1, review_user=user, review_podcast=podcast, podcast_rating=5, review_content="xxx")
    repo.add_review(review)

    # Fetch reviews for the podcast
    reviews = repo.get_reviews_for_podcast(1)

    # Assert: Ensure the review was retrieved correctly
    assert len(reviews) == 1  # There should be 1 review for the podcast.
    assert reviews[0]._content == "xxx"
    assert reviews[0]._rating == 5  # The review rating should be 5.

    review = Review(review_id=2, review_user=user, review_podcast=podcast, podcast_rating=4, review_content="yyy")
    repo.add_review(review)

    reviews = repo.get_reviews_for_podcast(1)

    # Checking that user made two reviews on podcast 1
    assert len(reviews) == 2
    assert reviews[1]._content == "yyy"
    assert reviews[1]._rating == 4  # The review rating should be 4.


def test_get_episodes_for_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Fetch episodes for the podcast
    episodes = repo.get_episodes_for_podcast(1)

    # Assert: Ensure the episodes were retrieved correctly
    assert len(episodes) == 3  # There should be 3 episodes for the podcast.
    assert episodes[0]._title == "Say It! Radio"  # First episode title should be 'Say It! Radio'.
    assert episodes[1]._title == "Say It! Radio"  # Second episode title should also be 'Say It! Radio'.

    # Assert: Ensure the episodes are indeed from podcast 1
    assert episodes[0]._podcast_id == 1
    assert episodes[1]._podcast_id == 1

    podcast = repo.get_podcast(1)

    # Add episodes with same ID to test
    episode1 = Episode(episode_id=1, podcast_id=1, title="Episode 1")
    episode2 = Episode(episode_id=2, podcast_id=1, title="Episode 2")
    repo.add_episode(episode1)
    repo.add_episode(episode2)

    # Fetch episodes for the podcast
    episodes = repo.get_episodes_for_podcast(1)


    # Assert: Ensure the correct number of episodes is returned
    assert len(episodes) == len(podcast.Podcast_episodes)
    assert episodes[0]._title == "Episode 1"
    assert episodes[1]._title == "Episode 2"


def test_get_random_podcasts(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Fetch random podcasts
    random_podcasts = repo.get_random_podcasts()

    # Assert: Ensure that up to 10 podcasts are returned as that is the limit
    assert len(random_podcasts) == 10


def test_get_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Add a user to the repository
    user = User(1, 'Alice', 'password')
    repo.add_user(user)

    # Fetch the user by username
    fetched_user = repo.get_user('Alice')

    # Assert: Ensure the user was fetched correctly
    assert fetched_user._username == 'Alice'


def test_get_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Add a user for the review
    user = User(user_id=1, username="testuser", password="password")
    repo.add_user(user)

    # Use an existing podcast from the database
    podcast = repo.get_podcast(1)

    # Add reviews to the repository
    review = Review(review_id=1, review_user=user, review_podcast=podcast, podcast_rating=5,
                    review_content="Great podcast!")
    repo.add_review(review)

    review2 = Review(review_id=2, review_user=user, review_podcast=podcast, podcast_rating=4, review_content="z")
    repo.add_review(review2)

    # Fetch all reviews
    reviews = repo.get_reviews()

    # Assert: Ensure the correct number of reviews is returned
    assert len(reviews) == 2
    assert reviews[0]._content == "Great podcast!"
    assert reviews[1]._content == "z"


def test_add_and_fetch_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Create user and playlist
    user = User(user_id=1, username="testuser", password="password")
    repo.add_user(user)

    playlist = Playlist(1, user, "My Playlist")

    # Add playlist to the repository
    repo.add_playlist(playlist)

    # Fetch the user's playlist
    fetched_playlist = repo.get_playlist_by_user(user)

    # Assert: Ensure the playlist was added and fetched correctly
    assert fetched_playlist.title == "My Playlist"
    # Check that the playlist retrieved is the same one that was added
    assert fetched_playlist == playlist


def test_update_users_playlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Create user and playlist
    user = User(user_id=1, username="testuser", password="password")
    repo.add_user(user)

    playlist = Playlist(1, user, "My Playlist")
    # Add playlist to the repository
    repo.add_playlist(playlist)

    users_playlist = repo.get_playlist_by_user(user)

    # Check that the playlist has no episodes
    assert users_playlist.list_of_episodes == []

    # Add episode from podcast 1
    episodes = repo.get_episodes_for_podcast(1)
    playlist.add_episode(episodes[1])

    # Update playlist
    repo.update_users_playlist(playlist)

    # Check that playlist has added episode
    assert playlist.list_of_episodes == [episodes[1]]
    # Check that playlist go updated in repo
    assert users_playlist._episodes == [episodes[1]]


def test_get_podcasts_sorted_alphabetically(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    sorted_podcasts = repo.get_podcasts_by_alphabet([])

    # Check first three is in alphabetical order
    assert sorted_podcasts[0]._title <= sorted_podcasts[1]._title
    assert sorted_podcasts[1]._title <= sorted_podcasts[2]._title
    assert sorted_podcasts[2]._title <= sorted_podcasts[3]._title


def test_add_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # check current amount of authors
    assert len(repo.get_authors()) == 9

    # Add author
    author = Author(10, "Neil")
    repo.add_author(author)

    # Check authors amount increased
    assert len(repo.get_authors()) == 10


def test_search_podcast_by_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # get list that is filter by the specific search
    filtered_list = repo.search_podcast_by_author("Audioboom")
    assert len(filtered_list) == 2  # Checking its correct length (2 Audioboom podcast)
    # Checking it is the correct podcast:
    assert filtered_list[0].title == "Crawlspace: True Crime & Mysteries"
    assert filtered_list[1].title == "AHDB"

    # Checking if there is nothing searched, it will just return an empty list
    nothing_list = repo.search_podcast_by_author("NotExist")
    assert nothing_list == []


def test_search_podcast_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # get list that is filter by the specific search
    filtered_list = repo.search_podcast_by_title("radio")
    assert len(filtered_list) == 3  # 3 podcast that has radio in its title
    # Checking that it is the correct podcasts
    assert filtered_list[0].title == "D-Hour Radio Network"
    assert filtered_list[1].title == "Brian Denny Radio"
    assert filtered_list[2].title == "Onde Road - Radio Popolare"

    # Checking if there is nothing searched, it will just return an empty list
    nothing_list = repo.search_podcast_by_author("NotExist")
    assert nothing_list == []


def test_search_podcast_by_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # get list that is filter by the specific search
    filtered_list = repo.search_podcast_by_category("Comedy")
    assert len(filtered_list) == 2  # 2 podcast has Comedy in its categories from test files

    # Checking that these podcast have Comedy category in them
    comedy_category = repo.get_category("Comedy")

    assert comedy_category in filtered_list[0].categories
    assert comedy_category in filtered_list[1].categories

    # Checking if there is nothing searched, it will just return an empty list
    nothing_list = repo.search_podcast_by_author("NotExist")
    assert nothing_list == []


def test_search_podcast_by_language(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # get list that is filter by the specific search
    filtered_list = repo.search_podcast_by_language("Italian")
    assert len(filtered_list) == 1  # Only 1 Italian podcast

    # Checking it is the right podcast
    assert filtered_list[0].title == "Onde Road - Radio Popolare"
    assert filtered_list[0].language == "Italian"

    # Checking if there is nothing searched, it will just return an empty list
    nothing_list = repo.search_podcast_by_author("NotExist")
    assert nothing_list == []