from sqlalchemy import text
from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist

from tests_db.conftest import session, empty_session

from datetime import datetime


# Creating inserts for tests to use
def insert_user(empty_session, values=None):
    new_username = "testuser"
    new_password = "password123"

    if values is not None:
        new_username = values[0]
        new_password = values[1]

    empty_session.execute(
        text('INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)'),
        {'username': new_username, 'password_hash': new_password}
    )
    row = empty_session.execute(
        text('SELECT user_id FROM users WHERE username = :username'),
        {'username': new_username}
    ).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute(
            text('INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)'),
            {'username': value[0], 'password_hash': value[1]}
        )
    rows = list(empty_session.execute(text('SELECT user_id FROM users')))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_podcast(empty_session):
    empty_session.execute(
        text('INSERT INTO podcasts (title, description, language, website_url) VALUES '
             '("Sample Podcast", "A sample podcast description", "English", "http://samplepodcast.com")')
    )
    row = empty_session.execute(text('SELECT podcast_id FROM podcasts')).fetchone()
    return row[0]


def insert_reviews(empty_session, podcast_key, user_key):
    timestamp_1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        text('INSERT INTO reviews (user_id, podcast_id, review_text, rating, timestamp) VALUES '
             '(:user_id, :podcast_id, "Great podcast!", 5, :timestamp_1),'
             '(:user_id, :podcast_id, "Not bad", 3, :timestamp_2)'),
        {'user_id': user_key, 'podcast_id': podcast_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute(text('SELECT review_id FROM reviews')).fetchone()
    return row[0]


def insert_categories(empty_session):
    empty_session.execute(
        text('INSERT INTO categories (category_name) VALUES ("Technology"), ("Education")')
    )
    rows = list(empty_session.execute(text('SELECT category_id FROM categories')))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_podcast_category_associations(empty_session, podcast_key, category_keys):
    stmt = text('INSERT INTO podcast_categories (podcast_id, category_id) VALUES (:podcast_id, :category_id)')
    for category_key in category_keys:
        empty_session.execute(stmt, {'podcast_id': podcast_key, 'category_id': category_key})


def insert_reviewed_podcast(empty_session):
    podcast_key = insert_podcast(empty_session)
    user_key = insert_user(empty_session)
    insert_reviews(empty_session, podcast_key, user_key)
    return podcast_key


def insert_episode(empty_session, podcast_key):
    empty_session.execute(
        text('INSERT INTO episodes (podcast_id, title, episode_link, episode_length, description, pub_date) VALUES '
             '(:podcast_id, "Sample Episode", "http://sampleepisode.com", 3600, "A sample episode description", :pub_date)'),
        {'podcast_id': podcast_key, 'pub_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    )
    row = empty_session.execute(text('SELECT episode_id FROM episodes')).fetchone()
    return row[0]


def insert_playlist(empty_session, user_key):
    empty_session.execute(
        text('INSERT INTO playlists (user_id, playlist_title) VALUES (:user_id, "Sample Playlist")'),
        {'user_id': user_key}
    )
    row = empty_session.execute(text('SELECT playlist_id FROM playlists')).fetchone()
    return row[0]


def insert_playlist_episode_associations(empty_session, playlist_key, episode_keys):
    stmt = text('INSERT INTO playlist_episodes (playlist_id, episode_id) VALUES (:playlist_id, :episode_id)')
    for episode_key in episode_keys:
        empty_session.execute(stmt, {'playlist_id': playlist_key, 'episode_id': episode_key})


def insert_authors(empty_session, values):
    connection = empty_session.connection()
    for value in values:
        connection.execute(
            text('INSERT INTO authors (author_id, name) VALUES (:author_id, :name)'),
            {'author_id': value[0], 'name': value[1]}
        )
    rows = list(connection.execute(text('SELECT author_id FROM authors')))
    keys = tuple(row[0] for row in rows)
    return keys


def test_author_mapping(session):
    # Test saving of authors
    author = Author(10086, "Joe Zhou")
    session.add(author)
    session.commit()

    # Retrieve authors from the database
    queried_author = session.query(Author).filter_by(_id=10086).one()
    assert queried_author.name == "Joe Zhou"


def test_podcast_mapping(session):
    author = Author(67890, "Alan Walker")
    podcast = Podcast(888, author, title="Fade")
    session.add(author)
    session.add(podcast)
    session.commit()

    # Retrieve podcasts from the database
    queried_podcast = session.query(Podcast).filter_by(_id=888).one()
    assert queried_podcast.title == "Fade"
    assert queried_podcast.author.name == "Alan Walker"


def test_category_mapping(session):
    category = Category(235, "CS235")
    session.add(category)
    session.commit()

    # Retrieve Category from the database
    queried_category = session.query(Category).filter_by(_id=235).one()
    assert queried_category.name == "CS235"


def test_user_mapping(session):
    user = User(1, "testuser", "password123")
    session.add(user)
    session.commit()

    # Retrieve Users from the database
    queried_user = session.query(User).filter_by(_id=1).one()
    assert queried_user.username == "testuser"


def test_review_mapping(session):
    user = User(1, "reviewer", "password123")
    podcast = Podcast(1, Author(1, "Author Name"), title="Podcast Review")
    review = Review(1, user, podcast, 5, "Great podcast!")
    session.add(user)
    session.add(podcast)
    session.add(review)
    session.commit()

    # Retrieve Review from the database
    queried_review = session.query(Review).filter_by(_id=1).one()
    assert queried_review.comment == "Great podcast!"
    assert queried_review.rating == 5


def test_playlist_mapping(session):
    user = User(1, "playlistuser", "password123")
    playlist = Playlist(1, user, "My Playlist")
    episode = Episode(1, 1, "Episode 1", "http://episode-link.com")
    playlist.add_episode(episode)
    session.add(user)
    session.add(playlist)
    session.add(episode)
    session.commit()

    # Retrieve Playlist from the database
    queried_playlist = session.query(Playlist).filter_by(_id=1).one()
    assert queried_playlist.title == "My Playlist"
    assert len(queried_playlist.list_of_episodes) == 1


def test_episode_mapping(session):
    podcast = Podcast(1, Author(1, "Author Name"), title="Podcast Title")
    episode = Episode(1, podcast.id, "Episode Title", "http://episode-link.com", 120)
    session.add(podcast)
    session.add(episode)
    session.commit()

    # Retrieve Episode from Database
    queried_episode = session.query(Episode).filter_by(_id=1).one()
    assert queried_episode.title == "Episode Title"
    assert queried_episode.link == "http://episode-link.com"
    assert queried_episode.length == 120


def test_loading_of_authors(empty_session):
    # Insert authors into the database
    authors = list()
    authors.append((1, "Author One"))
    authors.append((2, "Author Two"))
    insert_authors(empty_session, authors)

    # Expected authors
    expected = [
        Author(1, "Author One"),
        Author(2, "Author Two")
    ]

    # Assert that the authors are correctly loaded from the database
    assert empty_session.query(Author).all() == expected


def test_saving_of_authors(empty_session):
    # Create and add an author to the session
    author = Author(1, "Author One")
    empty_session.add(author)
    empty_session.commit()

    # Assert that the author is correctly saved in the database
    rows = list(empty_session.execute(text('SELECT author_id, name FROM authors')))
    assert rows == [(1, "Author One")]


def test_loading_of_podcasts(empty_session):
    # Insert a podcast into the database
    podcast_key = insert_podcast(empty_session)

    # Expected podcast
    expected_podcast = Podcast(podcast_key, "Sample Podcast", "A sample podcast description", "English",
                               "http://samplepodcast.com")

    # Assert that the podcast is correctly loaded from the database
    fetched_podcast = empty_session.query(Podcast).one()
    assert expected_podcast == fetched_podcast
    assert podcast_key == fetched_podcast._id


def test_saving_of_podcasts(empty_session):
    # Create and add an author to the session
    author = Author(1, "Sample Author")
    empty_session.add(author)
    empty_session.commit()

    # Create and add a podcast to the session
    podcast = Podcast(1, "Sample Podcast", "A sample podcast description", "English", "http://samplepodcast.com")
    podcast._author = author  # Set the author relationship
    empty_session.add(podcast)
    empty_session.commit()

    # Assert that the podcast is correctly saved in the database
    rows = list(
        empty_session.execute(text('SELECT podcast_id, title, description, language, website_url FROM podcasts')))
    assert rows == [(1, 'A sample podcast description', 'http://samplepodcast.com', 'Unspecified', '')]


def test_loading_of_categories(empty_session):
    # Insert categories into the database
    category_keys = insert_categories(empty_session)

    # Expected categories
    expected_categories = [
        Category(category_keys[0], "Technology"),
        Category(category_keys[1], "Education")
    ]

    # Assert that the categories are correctly loaded from the database
    fetched_categories = empty_session.query(Category).all()
    assert expected_categories == fetched_categories


def test_saving_of_categories(empty_session):
    # Create and add a category to the session
    category = Category(1, "Technology")
    empty_session.add(category)
    empty_session.commit()

    # Assert that the category is correctly saved in the database
    rows = list(empty_session.execute(text('SELECT category_id, category_name FROM categories')))
    assert rows == [(1, "Technology")]


def test_loading_of_reviews(empty_session):
    # Insert a podcast and a user into the database
    podcast_key = insert_podcast(empty_session)
    user_key = insert_user(empty_session)

    # Insert reviews into the database
    insert_reviews(empty_session, podcast_key, user_key)

    # Assert that the reviews are correctly loaded from the database
    reviews = empty_session.query(Review).all()
    assert len(reviews) == 2
    assert reviews[0]._content == "Great podcast!"
    assert reviews[1]._content == "Not bad"


def test_saving_of_reviews(empty_session):
    # Create and add an author to the session
    author = Author(1, "Sample Author")
    empty_session.add(author)
    empty_session.commit()

    # Create and add a podcast to the session
    podcast = Podcast(1, "Sample Podcast", "A sample podcast description", "English", "http://samplepodcast.com")
    podcast._author = author  # Set the author relationship
    empty_session.add(podcast)
    empty_session.commit()

    # Create and add a user to the session
    user = User(1, "testuser", "password123")
    empty_session.add(user)
    empty_session.commit()

    # Create and add a review to the session
    review = Review(1, user, podcast, 5, "Great podcast!", datetime.now())
    empty_session.add(review)
    empty_session.commit()

    # Assert that the review is correctly saved in the database
    rows = list(empty_session.execute(text('SELECT review_id, review_text, rating FROM reviews')))
    assert rows == [(1, "Great podcast!", 5)]


def test_loading_of_playlists(empty_session):
    # Insert a user into the database
    user_key = insert_user(empty_session)

    # Insert a playlist into the database
    playlist_key = insert_playlist(empty_session, user_key)

    # Expected playlist
    expected_playlist = Playlist(playlist_key, user_key, "Sample Playlist")

    # Assert that the playlist is correctly loaded from the database
    fetched_playlist = empty_session.query(Playlist).one()
    assert expected_playlist == fetched_playlist
    assert playlist_key == fetched_playlist._id


def test_saving_of_playlists(empty_session):
    # Create and add a user to the session
    user = User(1, "testuser", "password123")
    empty_session.add(user)
    empty_session.commit()

    # Create and add a playlist to the session
    playlist = Playlist(1, user, "Sample Playlist")
    empty_session.add(playlist)
    empty_session.commit()

    # Assert that the playlist is correctly saved in the database
    rows = list(empty_session.execute(text('SELECT playlist_id, playlist_title FROM playlists')))
    assert rows == [(1, "Sample Playlist")]


def test_loading_of_users(empty_session):
    # Insert users into the database
    users = list()
    users.append((1, "Andrew", "1234"))
    users.append((2, "Cindy", "1111"))
    insert_users(empty_session, users)

    # Expected users
    expected = [
        User(1, "Andrew", "1234"),
        User(2, "Cindy", "1111")
    ]

    # Assert that the users are correctly loaded from the database
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    # Create and add a user to the session
    user = User(1, "Andrew", "1234")
    empty_session.add(user)
    empty_session.commit()

    # Assert that the user is correctly saved in the database
    rows = list(empty_session.execute(text('SELECT user_id, username, password_hash FROM users')))
    assert rows == [(1, "Andrew", "1234")]


def test_saving_of_reviewed_podcast(empty_session):
    # Create and add an author to the session
    author = Author(1, "Sample Author")
    empty_session.add(author)
    empty_session.commit()

    # Create and add a podcast to the session
    podcast = Podcast(1, "Sample Podcast", "A sample podcast description", "English", "http://samplepodcast.com")
    podcast._author = author  # Set the author relationship
    empty_session.add(podcast)
    empty_session.commit()

    # Create and add a user to the session
    user = User(1, "testuser", "password123")
    empty_session.add(user)
    empty_session.commit()

    # Create and add a review to the session
    review = Review(1, user, podcast, 5, "Great podcast!", datetime.now())
    empty_session.add(review)
    empty_session.commit()

    # Assert that the review is correctly saved in the database
    rows = list(empty_session.execute(text('SELECT review_id, review_text, rating FROM reviews')))
    assert rows == [(1, "Great podcast!", 5)]


def test_loading_of_reviewed_podcast(empty_session):
    # Create and add an author to the session
    author = Author(1, "Sample Author")
    empty_session.add(author)
    empty_session.commit()

    # Create and add a podcast to the session
    podcast = Podcast(1, "Sample Podcast", "A sample podcast description", "English", "http://samplepodcast.com")
    podcast._author = author  # Set the author relationship
    empty_session.add(podcast)
    empty_session.commit()

    # Create and add a user to the session
    user = User(1, "testuser", "password123")
    empty_session.add(user)
    empty_session.commit()

    # Create and add a review to the session
    review = Review(1, user, podcast, 5, "Great podcast!", datetime.now())
    empty_session.add(review)
    empty_session.commit()

    # Assert that the podcast and review are correctly loaded from the database
    fetched_podcast = empty_session.query(Podcast).one()
    fetched_review = empty_session.query(Review).one()
    assert fetched_podcast == podcast
    assert fetched_review == review
    assert fetched_review.podcast == podcast
    assert fetched_review.reviewer == user


def test_loading_of_episodes(empty_session):
    # Create and add an author to the session
    author = Author(1, "Sample Author")
    empty_session.add(author)
    empty_session.commit()

    # Create and add a podcast to the session
    podcast = Podcast(1, "Sample Podcast", "A sample podcast description", "English", "http://samplepodcast.com")
    podcast._author = author  # Set the author relationship
    empty_session.add(podcast)
    empty_session.commit()

    # Insert an episode into the database
    episode_key = insert_episode(empty_session, podcast._id)

    # Expected episode
    expected_episode = Episode(episode_key, podcast._id, "Sample Episode", "http://sampleepisode.com", 3600,
                               "A sample episode description", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # Assert that the episode is correctly loaded from the database
    fetched_episode = empty_session.query(Episode).one()
    assert expected_episode == fetched_episode
    assert episode_key == fetched_episode._id


def test_saving_of_episodes(empty_session):
    # Create and add an author to the session
    author = Author(1, "Sample Author")
    empty_session.add(author)
    empty_session.commit()

    # Create and add a podcast to the session
    podcast = Podcast(1, "Sample Podcast", "A sample podcast description", "English", "http://samplepodcast.com")
    podcast._author = author  # Set the author relationship
    empty_session.add(podcast)
    empty_session.commit()

    # Create and add an episode to the session
    episode = Episode(1, podcast._id, "Sample Episode", "http://sampleepisode.com", 3600,
                      "A sample episode description", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    empty_session.add(episode)
    empty_session.commit()

    # Assert that the episode is correctly saved in the database
    rows = list(empty_session.execute(
        text('SELECT episode_id, title, episode_link, episode_length, description, pub_date FROM episodes')))
    assert rows == [(1, "Sample Episode", "http://sampleepisode.com", 3600, "A sample episode description",
                     datetime.now().strftime('%Y-%m-%d %H:%M:%S'))]
