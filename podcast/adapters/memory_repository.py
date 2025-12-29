import csv
import os
import random
from abc import ABC
from bisect import insort_left
# sorting by date
from datetime import datetime

from typing import List

from podcast.domainmodel.model import Author, Podcast, Category, User, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader

from podcast.adapters.repository import AbstractRepository, RepositoryException


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__podcasts = list()
        self.__podcasts_index = dict()
        self.__episodes = list()
        self.__episodes_index = dict()
        self.__users = list()
        self.__authors = set()
        self.__categories = set()
        self.__reviews = list()
        self.__playlists = list()
        self.__playlists_index = dict()

    def set_podcasts(self, podcasts: List[Podcast]):  # test done
        for podcast in podcasts:
            self.__podcasts_index[podcast.id] = podcast
        self.__podcasts = podcasts

    def add_podcast(self, podcast: Podcast):  # test done
        insort_left(self.__podcasts, podcast)
        self.__podcasts_index[podcast.id] = podcast

    def get_podcast(self, pod_id: int) -> Podcast:  # test done
        podcast = None

        try:
            podcast = self.__podcasts_index[pod_id]
        except KeyError:
            pass
        return podcast

    def get_podcasts(self) -> List[Podcast]:  # test done
        return self.__podcasts

    def add_episodes(self, episodes: List[Episode]):
        self.__episodes = episodes

    def add_episode(self, episode: Episode):
        insort_left(self.__episodes, episode)
        self.__episodes_index[episode.id] = episode

    def get_episode(self, ep_id: int) -> Episode:
        return self.__episodes[ep_id - 1]

    def get_list_of_podcasts_titles(self) -> List[str]:  # test done
        return [podcast.title for podcast in self.__podcasts]

    def get_podcasts_by_alphabet(self, list_of_titles):  # test done
        filtered_podcasts = [podcast for podcast in self.__podcasts if podcast.title in list_of_titles]

        # sorted_podcasts = sorted(filtered_podcasts, key=lambda podcast: podcast.title)

        # This is sorts it alphabetically but special characters
        # and numbers are at the end instead
        def custom_sort_key(podcast):
            title = podcast.title
            if title[0].isalpha():
                return 0, title.lower()
            else:
                return 1, title.lower()

        sorted_podcasts = sorted(filtered_podcasts, key=custom_sort_key)

        return sorted_podcasts

    def get_random_podcasts(self) -> List['Podcast']:  # test done
        limit = 10
        random.shuffle(self.__podcasts)

        return self.__podcasts[:limit]

    def get_podcasts_by_id(self) -> List['Podcast']:
        sorted_podcasts = sorted(self.__podcasts, key=lambda podcast: podcast.id)
        return sorted_podcasts

    def get_episodes_by_date(self, episodes: List[Episode]) -> List[Episode]:  # test done
        # Sort the episodes by their publication date
        sorted_episodes = sorted(episodes, key=lambda episode: datetime.strptime(episode.pub_date + '00',
                                                                                        '%Y-%m-%d %H:%M:%S%z'))
        return sorted_episodes

    def get_number_of_podcasts(self) -> int:
        return len(self.__podcasts)

    # Methods possibly used in next phases?

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username: str) -> User:
        return next((user for user in self.__users if user.username == username), None)

    def add_author(self, author: Author):
        self.__authors.add(author)

    def add_category(self, category: Category):
        self.__categories.add(category)

    def get_category(self, category_name) -> Category:
        return category_name

    def add_review(self, review: Review):
        self.__reviews.append(review)
        try:
            self.__podcasts_index[review.podcast.id].add_review(review)
        except KeyError:
            pass

    def get_review(self, review_name) -> Review:
        return review_name

    def add_playlist(self, playlist: Playlist):
        insort_left(self.__playlists, playlist)
        self.__playlists_index[playlist.user] = playlist

    def get_playlists(self) -> List[Playlist]:
        return self.__playlists

    def search_podcast_by_author(self, author_name: str) -> List[Podcast]:
        return [podcast for podcast in self.__podcasts if author_name.lower() in podcast.author.name.lower()]

    def search_podcast_by_category(self, category_name: str) -> List[Podcast]:
        return list({podcast.title: podcast for podcast in self.__podcasts for category in podcast.categories
                     if category_name.lower() in category.name.lower()}.values())

    def search_podcast_by_title(self, title_string: str) -> List[Podcast]:
        return [podcast for podcast in self.__podcasts if title_string.lower() in podcast.title.lower()]

    def search_podcast_by_language(self, language_string: str) -> List[Podcast]:
        return [podcast for podcast in self.__podcasts if language_string.lower() in podcast.language.lower()]

    #PHASE 2
    def get_playlist_by_user(self, user: User):
        for playlist in self.__playlists:
            if playlist.user == user:
                return playlist
        return None

    def get_number_of_episodes(self) -> int:
        return len(self.__episodes)

    def update_users_playlist(self, playlist: Playlist):
        self.__playlists_index[playlist.user] = playlist

    def get_reviews(self) -> List[Review]:
        return self.__reviews

    def get_reviews_for_podcast(self, podcast_id: int) -> List[Review]:
        return [review for review in self.__reviews if review.podcast.id == podcast_id]

    def add_multiple_categories(self, categories: set[Category]):
        for category in categories:
            self.add_category(category)

    def get_categories(self) -> List[Category]:
        pass

    def get_number_of_episodes_for_podcast(self, podcast_id: int) -> int:
        pass

    def get_episodes_for_podcast(self, podcast_id: int) -> List[Episode]:
        podcast = self.get_podcast(podcast_id)
        if podcast is None:
            return []

        episodes = [episode for episode in self.__episodes if episode.pod_id == podcast_id]
        return episodes

    def get_episodes(self) -> List[Episode]:
        pass

    def add_multiple_episodes(self, episode: List[Episode]):
        pass

    def add_multiple_podcasts(self, podcast: List[Podcast]):
        pass

    def get_number_of_authors(self):
        pass

    def get_authors(self) -> List[Author]:
        pass

    def add_multiple_authors(self, authors: set[Author]):
        for author in authors:
            self.add_author(author)
