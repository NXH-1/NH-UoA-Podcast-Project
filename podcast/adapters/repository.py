import abc
from typing import List

from podcast.domainmodel.model import Author, Podcast, Category, User, Episode, Review, Playlist

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):

    # region Author_data

    @abc.abstractmethod
    def add_author(self, author: Author):
        """ Add a single author to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_authors(self, author: set[Author]):
        """ Add multiple authors to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_authors(self) -> List[Author]:
        """ Returns the list of all authors. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_authors(self):
        """ Returns the number of authors in the repository. """
        raise NotImplementedError

    # endregion

    # region Podcast_data
    @abc.abstractmethod
    def add_podcast(self, podcast: Podcast):
        """ Add a single podcast to the repository of podcast. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_podcasts(self, podcast: List[Podcast]):
        """ Add multiple podcasts to the repository of podcast. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast(self, podcast_id: int) -> Podcast:
        """ Get a specific podcast by id. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts(self) -> List[Podcast]:
        """ Returns the list of podcast. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_podcasts(self) -> int:
        """ Returns the number of podcasts that exist in the repository. """
        raise NotImplementedError

    # endregion

    # region Episode_data
    @abc.abstractmethod
    def add_episode(self, episode: Episode):
        """ Add a single episode to the repository of episode. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_episodes(self, episode: List[Episode]):
        """ Add multiple episodes to the repository of episode. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_episode(self, episode_id: int) -> Episode:
        """ Get a specific episode by id. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes(self) -> List[Episode]:
        """ Returns the entire list of episodes. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes_for_podcast(self, podcast_id: int) -> List[Episode]:
        """Get all episodes for a specific podcast by podcast_id."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_episodes(self):
        """ Returns the total number of episode exist in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_episodes_for_podcast(self, podcast_id: int) -> int:
        """ Returns the number of episodes for a particular podcast by podcast_id. """
        raise NotImplementedError

    # endregion

    # region Category
    @abc.abstractmethod
    def get_categories(self) -> List[Category]:
        """ Return all categories that exist in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_category(self, category: Category):
        """ Add a category to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_categories(self, categories: set[Category]):
        """ Add many categories to the repository. """
        raise NotImplementedError

    # endregion

    @abc.abstractmethod
    def search_podcast_by_title(self, title_string: str) -> List[Podcast]:
        """Search for the podcast whose title includes the parameter title_string.
        It searches for the podcast title in case-insensitive and without trailing space.
        For example, the title 'Empire' will be searched if the title_string is 'empir'. """
        raise NotImplementedError

    @abc.abstractmethod
    def search_podcast_by_author(self, author_name: str) -> List[Podcast]:
        """Search for the podcast whose author contains the input author_name string.
        It searches for author names in case-insensitive and without trailing spaces.
        Returns searched podcast as a list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search_podcast_by_category(self, category_string: str) -> List[Podcast]:
        """Search for the podcast whose categories contain the input category_string.
        If any of the podcast's categories contain the substring category_string, that podcast should be selected for the search.
        It searches for category names in case-insensitive and without trailing spaces.
        Returns searched podcast as a list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search_podcast_by_language(self, language_string: str) -> List[Podcast]:
        """Search for list of podcasts that match given language
        Returns searched podcast as a list
        """
        raise NotImplementedError

    # stuff from mem_repo
    @abc.abstractmethod
    def set_podcasts(self, podcasts: List[Podcast]):
        raise NotImplementedError

    @abc.abstractmethod
    def get_list_of_podcasts_titles(self) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts_by_alphabet(self, list_of_names):
        raise NotImplementedError

    @abc.abstractmethod
    def get_category(self, category_name) -> Category:
        raise NotImplementedError

    @abc.abstractmethod
    def add_episodes(self, episode: List[Episode]):
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts_by_id(self) -> List[Podcast]:
        raise NotImplementedError

    @abc.abstractmethod
    def update_users_playlist(self, playlist: Playlist):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self) -> List[Review]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_for_podcast(self, podcast_id: int) -> List[Review]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_random_podcasts(self) -> List[Podcast]:
        raise NotImplementedError

    # authentication

    @abc.abstractmethod
    def add_user(self, new_user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlist_by_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def add_playlist(self, playlist: Playlist):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes_by_date(self, episodes: List[Episode]) -> List[Episode]:
        raise NotImplementedError
