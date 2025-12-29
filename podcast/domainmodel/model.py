from __future__ import annotations

import csv
from datetime import datetime
from typing import List


def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("ID must be a non-negative integer.")


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


class Author:
    def __init__(self, author_id: int, name: str):
        validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return f"<Author {self._id}: {self._name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.id)


class Podcast:
    def __init__(self, podcast_id: int, author: Author, title: str = "Untitled", image: str = None,
                 description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
        validate_non_negative_int(podcast_id)
        self._id = podcast_id
        self._author = author
        validate_non_empty_string(title, "Podcast title")
        self._title = title.strip()
        self._image = image
        self._description = description
        self._language = language
        self._website = website
        self._itunes_id = itunes_id
        self.categories = []
        self.episodes = []
        self.reviews = []  # List of reviews related to this podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def author(self) -> Author:
        return self._author

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category: Category):
        if category in self.categories:
            self.categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self.episodes:
            self.episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self.episodes:
            self.episodes.remove(episode)

    # Method to add a review to the podcast
    def add_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance.")
        self.reviews.append(review)

    def reviews(self) -> List[Review]:
        return self.reviews

    # Method to calculate the average rating
    def average_rating(self) -> float:
        if not self.reviews:
            return 0
        return sum([review.rating for review in self.reviews]) / len(self.reviews)

    def __repr__(self):
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.title < other.title

    def __hash__(self):
        return hash(self.id)

    @author.setter
    def author(self, value):
        self._author = value

    @itunes_id.setter
    def itunes_id(self, value):
        self._itunes_id = value


class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def __repr__(self) -> str:
        return f"<Category {self._id}: {self._name}>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._name < other.name

    def __hash__(self):
        return hash(self._id)


class User:
    def __init__(self, user_id: int, username: str, password: str):
        validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._id = user_id
        self._username = username.strip()
        self._password = password
        self._subscription_list = []
        self._reviews = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def subscription_list(self):
        return self._subscription_list

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))


class Episode:

    def __init__(self, episode_id: int, podcast_id: int, title: str = "untitled", episode_link: str = "",
                 episode_length: int = 0, episode_description: str = "", pub_date: str = ""):
        validate_non_negative_int(episode_id)
        validate_non_empty_string(title, "Episode title")
        self._id = episode_id
        self._podcast_id = podcast_id
        self._title = title.strip()
        self._link = episode_link
        self._length = episode_length
        self._description = episode_description
        self._pub_date = pub_date


    @property
    def id(self) -> int:
        return self._id

    @property
    def pod_id(self) -> int:
        return self._podcast_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def link(self) -> str:
        return self._link

    @property
    def length(self) -> int:
        return self._length

    @property
    def description(self) -> str:
        return self._description

    @property
    def pub_date(self) -> str:
        return self._pub_date

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Episode title")
        self._title = new_title.strip()

    @description.setter
    def description(self, new_description: str):
        validate_non_empty_string(new_description, "Episode description")
        self._description = new_description

    @link.setter
    def link(self, new_link: str):
        validate_non_empty_string(new_link, "Episode link")
        self._link = new_link

    def __repr__(self):
        return (
            f"<Episode ID: {self.id}. Podcast ID: {self.pod_id}. Title: {self.title}. "
            f"Episode length: {self._length}. Episode link: {self.link}. "
            f"Description: {self.description}. Pub Date: {self.pub_date}>")

    def __eq__(self, other):
        if not isinstance(other, Episode):
            return False
        return (self.id == other.id and self.title == other.title and self.link == other.link
                and self.length == other.length and self.description == other.description)

    def __lt__(self, other):
        if not isinstance(other, Episode):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.title, self.length, self.pub_date))


class Review:
    def __init__(self, review_id: int, review_user: User,
                 review_podcast: Podcast, podcast_rating: int,
                 review_content: str, timestamp: datetime = datetime.today()):
        # added this cause all other class have this
        # so probably id can't be negative
        validate_non_negative_int(review_id)
        # can't have negative rating
        validate_non_negative_int(podcast_rating)
        # since comment setter won't allow,
        # shouldn't be allowed to initiate it too
        validate_non_empty_string(review_content, "Review comment")
        self._id = review_id
        self._writer = review_user
        self._podcast = review_podcast
        self._rating = podcast_rating
        self._content = review_content
        self._timestamp = timestamp

    @property
    def id(self) -> int:
        return self._id

    # changed to return _id and return type to be int
    # so test accepts it

    @property
    def reviewer(self) -> User:
        return self._writer

    # Does reviewer need a setter, what if username is possibly changed?

    # I think it does not, as initialise with User object so if User changes name,
    # then it will change name here too

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @property
    def rating(self) -> int:
        return self._rating

    @property
    def comment(self) -> str:
        return self._content

    @property
    def timestamp(self):
        return self._timestamp

    def time_to_current_timestamp(self):
        self._timestamp = datetime.today()

    @rating.setter
    def rating(self, new_rating: int):
        validate_non_negative_int(new_rating)
        if not (0 <= new_rating <= 10):
            raise ValueError("Rating must be an integer between 0 and 10")
        self._rating = new_rating

    # what type of rating system do we want? I think the rating will be added
    # in a list of float/integer and summed, averaged to find rating of podcast

    @comment.setter
    def comment(self, new_comment):
        validate_non_empty_string(new_comment, "Review comment")
        self._content = new_comment

    def __repr__(self):
        return (f"<Reviewer: {self._writer}"
                f"Podcast rating: {self._rating}.\nComment: {self._content}.>")

    # Format issues? What does it look like when shown?

    # This is an example of what it looks like:
    # <Reviewer: <User 1: shyamli> Podcast rating: 5."
    # Comment: I thought...>

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self._id == other._id

    # Does the eq method only compare id or does it compare every instance?

    # Looking at other classes, I think it would make sense for It only compare id
    # because id should be completely unique to a certain object whereas others could
    # possibly be the same

    # Yeah I thought so too, I've changed eq method to only compare ID

    def __lt__(self, other):
        if not isinstance(other, Review):
            return False
        return self._id < other._id

    def __hash__(self):
        return hash(self._id)


class Playlist:
    # added initialise with a preset title if not given one
    def __init__(self, playlist_id: int, playlist_user: User, playlist_title: str = "Untitled playlist"):
        # added same thing as previous class
        validate_non_negative_int(playlist_id)
        # so no empty titles
        validate_non_empty_string(playlist_title, "Playlist title")
        self._id = playlist_id
        self._user = playlist_user
        self._title = playlist_title
        self._episodes = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def user(self) -> User:
        return self._user

    @property
    def title(self) -> str:
        return self._title

    # Added variable types, changed to names use in initialisation

    @property
    def list_of_episodes(self):
        return self._episodes

    # how does returning a list work in python?

    # In string format, it will be [] if its empty
    # you can also it to a variable like: playlist1 = Playlist.list_of_episodes

    @title.setter
    def title(self, new_title):
        validate_non_empty_string(new_title, "Playlist title")
        self._title = new_title

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self._episodes:
            self._episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self._episodes:
            self._episodes.remove(episode)

    def __repr__(self):
        return (f"<Playlist title: {self._title}, "
                f"Playlist creator: {self.user}.\nEpisodes: {self._episodes}.>")

    # Check formatting

    # Will print out the following:
    # <Playlist title: My First Playlist, Playlist creator: <User 1: shyamli>
    # Episodes: [].>

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self._id == other._id

    def __lt__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self._id < other._id

    def __hash__(self):
        return hash(self._id)
