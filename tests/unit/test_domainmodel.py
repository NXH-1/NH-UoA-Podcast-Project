import pytest
# For file pathing
import os
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from datetime import datetime, timedelta

from podcast.adapters.datareader.csvdatareader import CSVDataReader


# Test for Author Initialization
def test_author_initialization():
    # Creating a valid author
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"  # Check the string representation of the object
    assert author1.name == "Brian Denny"  # Check that the name was set correctly

    # Test invalid Author creation - empty name
    with pytest.raises(ValueError):
        author2 = Author(2, "")

    # Test invalid Author creation - non-string name
    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    # Check if spaces in name are removed
    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    # Test setting a new name for an Author
    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"  # Verify the change


# Test for Author Equality
def test_author_eq():
    # Equality comparison between two Author objects
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2  # Same ID, so they are considered equal
    assert author1 != author3  # Different IDs
    assert author3 != author2  # Different IDs
    assert author3 == author3  # Same object should always be equal to itself

# Test for Author Comparison using less than (<) operator
def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2  # Based on name comparison
    assert author2 > author3  # Name sorting comparison
    assert author1 < author3  # Name sorting comparison

    # Test sorting of a list of Author objects
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


# Test for Author Hashing (useful for sets/dicts)
def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)  # Add authors to set
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3  # Verify set contains 3 unique authors

    # Verify sorted order of the authors in the set
    assert repr(sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"

    # Remove an author and verify the change
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


# Test setting and validation of Author name
def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "  # Leading/trailing spaces should be trimmed
    assert repr(author) == "<Author 1: USA Radio>"

    # Test invalid name setting (empty name)
    with pytest.raises(ValueError):
        author.name = ""

    # Test invalid name setting (non-string name)
    with pytest.raises(ValueError):
        author.name = 123


# Test for Category Initialization
def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"  # Verify the string representation
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"  # Spaces should be removed

    # Test invalid Category creation
    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    # Test trimming spaces for Category name
    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    # Test invalid Category name (empty)
    with pytest.raises(ValueError):
        category1 = Category(4, "")


# Test Category name setting and validation
def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    # Test invalid Category name setting (empty or non-string)
    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


# Test for Category Equality
def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1  # Same object should always be equal to itself
    assert category1 != category2  # Different objects with different names
    assert category2 != category3
    assert category1 != "9: Adventure"  # Ensure type-safe comparison
    assert category2 != 105  # Ensure type-safe comparison


# Test Category Hashing
def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()  # Create a set of categories
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)

    # Verify all categories are in the set
    assert sorted(category_set) == [category1, category2, category3]

    # Remove categories from the set and verify
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


# Test Category Comparison using less than (<) operator
def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2  # Sort by name
    assert category2 < category3
    assert category3 > category1

    # Test sorting a list of categories
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures (used for creating objects that will be used in multiple tests)
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


@pytest.fixture
def my_episode(my_podcast):
    return Episode(1, my_podcast.id)


@pytest.fixture
def my_review(my_user, my_podcast):
    return Review(1, my_user, my_podcast, 5, "hello")


@pytest.fixture
def my_playlist(my_user):
    return Playlist(1, my_user, "playlist1")


# Test for Podcast Initialization
def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")

    # Check initialization attributes
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    # Verify the string representation of the Podcast
    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    # Test invalid Podcast creation
    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, "Todd Clayton")

    podcast4 = Podcast(123, " ")
    assert podcast4.title == 'Untitled'  # Default title for empty string
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    # Test changing the title of the podcast.
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    # Test that an empty title raises a ValueError.
    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    # Test adding a category to the podcast.
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    # Test that adding the same category multiple times doesn't duplicate it.
    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    # Test removing a category from the podcast.
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    # Test that removing a non-existing category doesn't affect the list.
    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    # Test setting a new valid title for the podcast.
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    # Test that setting an invalid title (empty or spaces) raises a ValueError.
    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    # Test equality of two podcasts based on their ID.
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")

    assert podcast1 == podcast1  # Same object comparison
    assert podcast1 != podcast2  # Different ID
    assert podcast2 != podcast3  # Different ID


def test_podcast_hash():
    # Test hashing of podcasts based on their ID. Podcasts with the same ID should have the same hash.
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")  # Same ID as podcast1
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}

    # Only two unique podcasts should be in the set because podcast1 and podcast2 have the same ID.
    assert len(podcast_set) == 2


def test_podcast_lt():
    # Test the comparison of podcasts using the less-than operator based on their ID.
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")

    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    # Test the initialization of a User object.
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")

    # Test that the username is properly formatted.
    assert repr(user1) == "<User 1: Shyamli>"
    assert repr(user2) == "<User 2: asma>"
    assert repr(user3) == "<User 3: JeNNy>"

    # Test that an empty password or username raises a ValueError.
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    # Test equality of users based on their ID.
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")

    assert user1 == user4  # Same ID
    assert user1 != user2  # Different ID
    assert user2 != user3  # Different ID


def test_user_hash():
    # Test hashing of User objects based on their ID. Users with the same ID should have the same hash.
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")

    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)

    # The users should be sorted and the set should contain only unique users.
    assert sorted(user_set) == [user1, user2, user3]

    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    # Test the comparison of users using the less-than operator based on their ID.
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")

    assert user1 < user2
    assert user2 < user3
    assert user3 > user1

    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    # Test adding and removing podcast subscriptions for a user.
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by Shyamli>]"

    # Ensure the same subscription is not added multiple times.
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1

    # Test removing the subscription.
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_podcast_subscription_initialization(my_subscription):
    # Test the initialization of a PodcastSubscription object.
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "<User 1: Shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"
    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by Shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    # Test setting a new owner for the subscription.
    new_user = User(2, "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    # Test that setting an invalid owner raises a TypeError.
    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    # Test setting a new podcast for the subscription.
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    # Test that setting an invalid podcast raises a TypeError.
    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    # Test equality of podcast subscriptions based on their ID.
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)

    assert sub1 == sub2  # Same ID
    assert sub1 != sub3  # Different ID


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1


# TODO : Write Unit Tests for CSVDataReader, Episode, Review, Playlist classes

#
def test_episode_initialization():
    # Test the initialization of an Episode object with valid data.
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    episode1 = Episode(1, podcast1.id, "title",
                       "www.website.com", 20,
                       "This is about..", "13/08/2024")

    # Verify the Episode attributes are correctly set.
    assert episode1.id == 1
    assert episode1.pod_id == podcast1.id
    assert episode1.title == "title"
    assert episode1.link == "www.website.com"
    assert episode1.description == "This is about.."
    assert episode1.pub_date == "13/08/2024"

    # Check the string representation of the Episode object.
    assert repr(episode1) == ("<Episode ID: 1. "
                              "Podcast ID: 2. Title: title. "
                              "Episode length: 20. Episode link: www.website.com. "
                              "Description: This is about... Pub Date: 13/08/2024>")

    # Test invalid Episode initializations with negative ID and empty title.
    with pytest.raises(ValueError):
        episode2 = Episode(-2, 2, "title",
                           "www.website.com", 20,
                           "This is about..", "13/08/2024")
    with pytest.raises(ValueError):
        episode3 = Episode(3, 2, "")

    # Test default values when an Episode is initialized with minimal parameters.
    episode4 = Episode(4, 2)
    assert episode4.title == "untitled"
    assert episode4.link == ""
    assert episode4.length == 0
    assert episode4.description == ""
    assert episode4.pub_date == ""


def test_episode_change_title(my_episode):
    # Test the ability to change the title of an episode.
    my_episode.title = "Episode title"
    assert my_episode.title == "Episode title"

    # Test setting an invalid (empty) title.
    with pytest.raises(ValueError):
        my_episode.title = ""


def test_episode_change_description(my_episode):
    # Test changing the description of an episode.
    my_episode.description = "Episode description"
    assert my_episode.description == "Episode description"

    # Test setting an invalid (empty) description.
    with pytest.raises(ValueError):
        my_episode.description = ""


def test_episode_change_link(my_episode):
    # Test changing the link of an episode.
    my_episode.link = "Episode link"
    assert my_episode.link == "Episode link"

    # Test setting an invalid (empty) link.
    with pytest.raises(ValueError):
        my_episode.link = ""


def test_episode_equality(my_episode):
    # Test episode equality based on IDs.
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    episode1 = Episode(1, podcast1.id, "title")
    episode2 = Episode(2, podcast1.id, "second")
    episode3 = Episode(3, podcast1.id, "third")
    dupe_episode1 = Episode(1, podcast1.id, "title")
    string_instance = "hello"

    # Check equality between episodes.
    assert episode1 == episode1
    assert episode1 == dupe_episode1
    assert episode2 != episode1
    assert episode3 != episode2
    assert episode3 != string_instance


def test_episode_lt(my_episode):
    # Test comparison (less than) between episode IDs.
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    episode1 = Episode(1, podcast1.id, "title")
    episode2 = Episode(2, podcast1.id, "second")
    episode3 = Episode(3, podcast1.id, "third")
    dupe_episode1 = Episode(1, podcast1.id, "title")

    # Verify that episodes are correctly compared based on ID.
    assert episode1.id < episode2.id
    assert episode1.id < episode3.id
    assert episode2.id < episode3.id


def test_episode_hash():
    # Test the hashing of Episode objects.
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    episode1 = Episode(1, podcast1.id, "title")
    episode2 = Episode(2, podcast1.id, "second")
    episode3 = Episode(3, podcast1.id, "third")
    dupe_episode1 = Episode(1, podcast1.id, "title")

    # Test that episode hashes are unique for different episodes and not duplicated.
    podcast_set = {episode1, episode2, episode3}
    podcast_set2 = {episode1, episode2, episode3, dupe_episode1}
    assert len(podcast_set) == 3
    assert len(podcast_set2) == 3


def test_review_initialization():
    # Test the initialization of a Review object.
    user1 = User(1, "Shyamli", "pw12345")
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    review1 = Review(1, user1, podcast1, 5, "I thought..")

    # Verify the review attributes are correctly set.
    assert review1.id == 1
    assert review1.reviewer == user1
    assert review1.podcast == podcast1
    assert review1.rating == 5
    assert review1.comment == "I thought.."

    # Check the string representation of the Review object.
    assert repr(review1) == ("<Reviewer: <User 1: Shyamli>"
                             "Podcast rating: 5.\n"
                             "Comment: I thought...>")

    # Test invalid Review initializations (negative ID, empty comment, invalid rating).
    with pytest.raises(ValueError):
        review2 = Review(-1, user1, podcast1, 5, "a")
    with pytest.raises(ValueError):
        review3 = Review(2, user1, podcast1, 5, "")
    with pytest.raises(ValueError):
        review4 = Review(1, user1, podcast1, -5, "no")


def test_review_rating_change(my_review):
    # Test changing the rating of a review.
    my_review.rating = 8
    assert my_review.rating == 8

    # Test setting invalid ratings.
    with pytest.raises(ValueError):
        my_review.rating = -1
    with pytest.raises(ValueError):
        my_review.rating = 11


def test_review_comment_edit(my_review):
    # Test changing the comment of a review.
    my_review.comment = "It's okay"
    assert my_review.comment == "It's okay"

    # Test setting an invalid (empty) comment.
    with pytest.raises(ValueError):
        my_review.comment = ""


def test_add_review():
    # Test adding reviews to a podcast.
    author = Author(1, "Doctor Squee")
    podcast = Podcast(1, author, "Podcast Title")

    # Create users and reviews.
    user1 = User(1, "JohnDoe", "password123")
    review1 = Review(1, user1, podcast, 5, "Great Podcast!")
    user2 = User(2, "JaneDoe", "password456")
    review2 = Review(2, user2, podcast, 4, "Really enjoyed this.")

    # Add reviews to the podcast and verify.
    podcast.add_review(review1)
    assert podcast.reviews == [review1]
    podcast.add_review(review2)
    assert podcast.reviews == [review1, review2]

    # Test that adding invalid data (non-review) raises a TypeError.
    try:
        podcast.add_review("This is not a review")
        assert False, "TypeError was not raised for an invalid review"
    except TypeError:
        assert True  # Expected behavior


def test_average_rating():
    # Test calculating the average rating of a podcast.
    author = Author(1, "Doctor Squee")
    podcast = Podcast(1, author, "Podcast Title")

    # Initially, the podcast should have no reviews and the average rating should be 0.
    assert podcast.average_rating() == 0

    # Create users and reviews.
    user1 = User(1, "JohnDoe", "password123")
    review1 = Review(1, user1, podcast, 5, "Great Podcast!")
    user2 = User(2, "JaneDoe", "password456")
    review2 = Review(2, user2, podcast, 4, "Really enjoyed this.")

    # Add reviews and calculate average rating.
    podcast.add_review(review1)
    assert podcast.average_rating() == 5.0  # Only one review, average is 5.
    podcast.add_review(review2)
    assert podcast.average_rating() == 4.5  # Average of 5 and 4.


def test_review_timestamp():
    # Test that a review is initialized with the correct timestamp
    user1 = User(1, "Shyamli", "pw12345")
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    current_time = datetime.today()

    review1 = Review(1, user1, podcast1, 5, "This is a great podcast!", current_time)

    # Ensure the timestamp is initialized correctly
    assert review1.timestamp == current_time


def test_review_time_to_current_timestamp():
    # Test that the time_to_current_timestamp updates the timestamp correctly
    user1 = User(1, "Shyamli", "pw12345")
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    initial_time = datetime.today() - timedelta(days=1)  # Set the timestamp 1 day earlier

    # Create a review with an old timestamp
    review1 = Review(1, user1, podcast1, 5, "Interesting podcast!", initial_time)

    # Ensure the timestamp is initially set to the old timestamp
    assert review1.timestamp == initial_time

    # Call the method to update the timestamp to the current time
    review1.time_to_current_timestamp()

    # Ensure the timestamp has been updated to the current time (or close to it)
    current_time = datetime.today()
    assert review1.timestamp.date() == current_time.date()  # Check if the date is the same as today
    assert review1.timestamp.time().hour == current_time.time().hour  # Check the hour to ensure it's updated


def test_review_equality(my_review):
    # Create two users and a podcast to use for creating reviews
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "other", "pw12345")
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")

    # Create two reviews with the same ID and content to check equality
    review1 = Review(1, user1, podcast1, 5, "I thought..")
    review1_copy = Review(1, user1, podcast1, 5, "I thought..")

    # Create a third review with a different ID and content
    review2 = Review(2, user2, podcast1, 2, "hey")

    # Check that 'my_review' is equal to 'review1' (assuming 'my_review' has the same ID and content)
    assert my_review == review1

    # Test that reviews with the same ID are considered equal
    assert review1 == review1_copy

    # Test that reviews with different IDs are not equal
    assert review1 != review2

    # Test that a review is not equal to an instance of a different type
    assert review1 != "Not a review"


def test_review_lt(my_review):
    # Create two users and a podcast
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "other", "pw12345")
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")

    # Create two reviews, one with a lower ID and another with a higher ID
    review1 = Review(1, user1, podcast1, 5, "I thought..")
    review2 = Review(2, user2, podcast1, 2, "hey")

    # Check if 'my_review' is less than 'review2' (assuming 'my_review' has a lower ID)
    assert my_review < review2

    # Test that review1 (with lower ID) is less than review2 (with higher ID)
    assert review1 < review2


def test_review_hash():
    # Create two users and a podcast
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "other", "pw12345")
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")

    # Create three unique reviews
    review1 = Review(1, user1, podcast1, 5, "I thought..")
    review2 = Review(2, user2, podcast1, 2, "hey")
    review3 = Review(3, user2, podcast1, 4, "Hello")

    # Create a duplicate of review1 (same ID and content)
    review1dupe = Review(1, user1, podcast1, 5, "I thought..")

    # Test that adding 'review1' and its duplicate to a set results in only one unique review
    review_set = {review1, review1dupe}
    assert len(review_set) == 1  # The set should only contain one unique review

    # Test adding multiple unique reviews to a set, ensuring all are counted
    review_set2 = {review1, review1dupe, review2, review3}
    assert len(review_set2) == 3  # The set should contain 3 unique reviews (review1 and
    # review1dupe are considered equal)


def test_playlist_initialization():
    # Create a user and initialize a playlist with a title and ID
    user1 = User(1, "Shyamli", "pw12345")
    playlist1 = Playlist(1, user1, "My First Playlist")

    # Assert that the playlist ID and title are correctly initialized
    assert playlist1.id == 1
    assert playlist1.title == "My First Playlist"

    # Check the representation of the playlist
    assert repr(playlist1) == ("<Playlist title: My First Playlist, "
                               "Playlist creator: <User 1: Shyamli>.\n"
                               "Episodes: [].>")

    # Ensure a ValueError is raised for invalid playlist IDs
    with pytest.raises(ValueError):
        playlist2 = Playlist(-2, user1, "My second Playlist")

    # Test playlist initialization without a title
    playlist3 = Playlist(3, user1)
    assert playlist3.id == 3
    assert playlist3.title == "Untitled playlist"


def test_playlist_change_title(my_playlist):
    # Set and verify a new title for the playlist
    my_playlist.title = "My First Playlist"
    assert my_playlist.title == "My First Playlist"

    # Test that a ValueError is raised if the title is set to an empty string
    with pytest.raises(ValueError):
        my_playlist.title = ""


def test_playlist_add_episode(my_playlist):
    # Create an author, a podcast, and some episodes to add to the playlist
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    episode1 = Episode(1, podcast1.id, "title")
    episode2 = Episode(2, podcast1.id, "second")
    episode3 = Episode(3, podcast1.id, "third")

    # Test that a TypeError is raised when adding something other than an episode
    with pytest.raises(TypeError):
        my_playlist.add_episode(author1)

    # Add the episodes to the playlist and assert they are correctly added
    my_playlist.add_episode(episode1)
    assert len(my_playlist.list_of_episodes) == 1
    assert my_playlist.list_of_episodes == [episode1]

    # Add multiple episodes and ensure the playlist contains them
    my_playlist.add_episode(episode2)
    my_playlist.add_episode(episode3)
    assert my_playlist.list_of_episodes == [episode1, episode2, episode3]

    # Adding the same episode again should not increase the count
    my_playlist.add_episode(episode1)
    assert len(my_playlist.list_of_episodes) == 3
    assert my_playlist.list_of_episodes == [episode1, episode2, episode3]


def test_playlist_remove_episode(my_playlist):
    # Create episodes to add and remove from the playlist
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    episode1 = Episode(1, podcast1.id, "title")
    episode2 = Episode(2, podcast1.id, "second")
    episode3 = Episode(3, podcast1.id, "third")
    episode4 = Episode(4, podcast1.id, "fourth")

    # Add episodes to the playlist
    my_playlist.add_episode(episode1)
    my_playlist.add_episode(episode2)
    my_playlist.add_episode(episode3)

    # Try to remove an episode that is not in the playlist
    my_playlist.remove_episode(episode4)
    assert my_playlist.list_of_episodes == [episode1, episode2, episode3]

    # Remove episodes from the playlist and assert they are removed correctly
    my_playlist.remove_episode(episode2)
    assert my_playlist.list_of_episodes == [episode1, episode3]
    my_playlist.remove_episode(episode1)
    my_playlist.remove_episode(episode3)
    assert my_playlist.list_of_episodes == []
    assert len(my_playlist.list_of_episodes) == 0


def test_playlist_equality(my_playlist):
    # Create two playlists with different IDs and check equality
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    episode1 = Episode(1, podcast1.id, "title")
    episode2 = Episode(2, podcast1.id, "second")
    episode3 = Episode(3, podcast1.id, "third")
    episode4 = Episode(4, podcast1.id, "fourth")
    user1 = User(1, "Shyamli", "pw12345")
    playlist1 = Playlist(2, user1, "My First Playlist")
    playlist2 = Playlist(1, user1, "My First Playlist")

    # Ensure that playlists with different IDs are not equal
    assert playlist1 == playlist1
    assert my_playlist != playlist1
    assert my_playlist == playlist2

    # Test that comparing with an invalid type returns False
    not_right_instance = my_playlist == 1
    assert not_right_instance == False


def test_playlist_lt(my_playlist):
    # Create playlists with different IDs and check if the order is correct
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    episode1 = Episode(1, podcast1.id, "title")
    episode2 = Episode(2, podcast1.id, "second")
    episode3 = Episode(3, podcast1.id, "third")
    episode4 = Episode(4, podcast1.id, "fourth")
    user1 = User(1, "Shyamli", "pw12345")
    playlist1 = Playlist(2, user1, "My First Playlist")
    playlist2 = Playlist(1, user1, "My First Playlist")
    playlist3 = Playlist(3, user1, "My Second Playlist")

    # Test that playlists are ordered correctly by ID
    assert playlist2 < playlist1
    assert my_playlist < playlist1
    assert playlist1 < playlist3
    assert playlist2 < playlist3

    # Test that comparing with an invalid type returns False
    not_right_instance = my_playlist < 2
    assert not_right_instance == False


# Testing the playlist Hashing
def test_playlist_hash():
    # Create playlists and test hash uniqueness
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    episode1 = Episode(1, podcast1.id, "title")
    episode2 = Episode(2, podcast1.id, "second")
    episode3 = Episode(3, podcast1.id, "third")
    episode4 = Episode(4, podcast1.id, "fourth")
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "other", "pw12345")

    # Create multiple playlists to check hash uniqueness
    playlist1 = Playlist(2, user1, "My First Playlist")
    playlist2 = Playlist(1, user1, "My First Playlist")
    playlist3 = Playlist(3, user1, "My Second Playlist")
    playlist4 = Playlist(4, user2, "My Second Playlist")
    playlist5 = Playlist(2, user2, "My Second Playlist")

    # Test that playlists with the same ID produce the same hash
    assert hash(playlist1) == hash(playlist5)

    # Test that unique playlists are counted correctly in a set
    playlist_set = {playlist1, playlist2, playlist3, playlist4, playlist5}
    assert len(playlist_set) == 4  # Only unique playlists should be counted

    # Test that duplicates are handled correctly in the set
    playlist_set2 = {playlist1, playlist5}
    assert len(playlist_set2) == 1  # playlist1 and playlist5 have the same ID, so only 1 unique hash


# testing CSV reader's initialization
def test_CSVReader_initialization():
    reader1 = CSVDataReader("../data/episodes.csv",
                            "../data/podcasts.csv")
    assert reader1.episode_file_path == "../data/episodes.csv"  # Seeing if the file path is the same as given
    assert reader1.podcast_file_path == "../data/podcasts.csv"


# Testing CSV reader capability of retrieving episodes info
def test_CSVReader_read_episodes():
    dir_name = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dir_name)
    reader1 = CSVDataReader("../data/episodes.csv",
                            '../data/podcasts.csv')  # gets the data
    reader1.read_podcasts() # needs to call read podcast first so episodes can lookup podcast
    reader1.read_episodes()
    assert reader1.dataset_of_episodes[0].id == 1  # Checking if it has expected ID
    assert reader1.dataset_of_episodes[0].pod_id == 14 # Checking that it aligns with the correct podcast
    assert reader1.dataset_of_episodes[1].id == 70
    assert reader1.dataset_of_episodes[1].pod_id == 2
    assert reader1.dataset_of_episodes[
               0].title == ('The Mandarian Orange Show Episode 74- Bad Hammer Time,'
                            ' or: 30 Day MoviePass Challenge Part 3')   # Checking if it has the expected title


# testing CSV reader capability of retrieving podcast info from CSV
def test_CSVReader_read_podcast():
    dir_name = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dir_name)
    reader1 = CSVDataReader("../data/episodes.csv",
                            "../data/podcasts.csv")  # get the info with CSV
    reader1.read_podcasts()


    assert reader1.dataset_of_podcasts[0].id == 1  # test if it got the podcast and by the expected order (default is by ID)
    assert reader1.dataset_of_podcasts[0].title == 'D-Hour Radio Network'  # testing if it matches with ID
    assert reader1.dataset_of_podcasts[1].id == 2
    assert reader1.dataset_of_podcasts[1].title == 'Brian Denny Radio'
    assert repr(reader1.dataset_of_podcasts[0].author) == "<Author 1: D Hour Radio Network>"   # testing if it contains correct author
    assert reader1.dataset_of_podcasts[7].id == 23
    assert repr(reader1.dataset_of_podcasts[7].author) == "<Author 8: Audioboom>"
    assert reader1.dataset_of_podcasts[8].id == 100
    assert repr(reader1.dataset_of_podcasts[8].author) == "<Author 8: Audioboom>"
    c1 = Category(1, 'Society & Culture')
    c2 = Category(2, 'Personal Journals')
    c3 = Category(3, 'Professional')
    c4 = Category(4, 'News & Politics')
    c5 = Category(5, 'Sports & Recreation')
    c6 = Category(6, 'Comedy')
    assert reader1.dataset_of_podcasts[0].categories == [c1, c2]   # Checking if it has the all the correct categories
    assert reader1.dataset_of_podcasts[1].categories == [c3, c4, c5, c6]
    assert repr(reader1.dataset_of_podcasts[9].author) == "<Author 9: Unknown author>"  # all null authors will be this
    assert reader1.dataset_of_podcasts[9].title == "Locked on Cubs"    # Checking unknown author has matching title
    assert repr(reader1.dataset_of_podcasts[10].author) == "<Author 9: Unknown author>"    # testing that other unknown author has same ID
    assert reader1.dataset_of_podcasts[10].title == "Montvale Evangelical Free Church Podcast"
