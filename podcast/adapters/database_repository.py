from abc import ABC
from typing import List, Type

from sqlalchemy import func, case
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist


# feature 1 test
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # region Podcast_data
    def get_podcasts(self, sorting: bool = False) -> List[Podcast]:
        podcasts = self._session_cm.session.query(Podcast).all()
        return podcasts

    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            query = self._session_cm.session.query(Podcast).filter(
                Podcast._id == podcast_id)
            podcast = query.one()
        except NoResultFound:
            print(f'Podcast {podcast_id} was not found')

        return podcast

    def add_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            scm.session.merge(podcast)
            scm.commit()

    def add_multiple_podcasts(self, podcasts: List[Podcast]):
        with self._session_cm as scm:
            for podcast in podcasts:
                scm.session.add(podcast)
            scm.commit()

    def get_number_of_podcasts(self) -> int:
        num_podcasts = self._session_cm.session.query(Podcast).count()
        return num_podcasts

    # endregion

    # region Author data
    def get_authors(self) -> List[Author]:
        authors = self._session_cm.session.query(Author).all()
        return authors

    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.merge(author)
            scm.commit()

    def add_multiple_authors(self, authors: List[Author]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    existing_author = scm.session.query(Author).filter_by(name=author.name).first()
                    if existing_author:
                        print(f"Author '{author.name}' already exists, skipping.")
                        continue
                    scm.session.add(author)
            scm.commit()

    def get_number_of_authors(self) -> int:
        num_authors = self._session_cm.session.query(Author).count()
        return num_authors

    # endregion

    # region Category_data
    def get_categories(self) -> list[Type[Category]]:
        categories = self._session_cm.session.query(Category).all()
        return categories

    def add_category(self, category: Category):
        with self._session_cm as scm:
            scm.session.merge(category)
            scm.commit()

    def add_multiple_categories(self, categories: List[Category]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for category in categories:
                    scm.session.add(category)
            scm.commit()

    # endregion

    # region Episode_data
    def get_episodes(self, sorting: bool = False) -> list[Type[Episode]]:
        episodes = self._session_cm.session.query(Episode).all()
        return episodes

    def get_episode(self, episode_id: int) -> Episode:
        episode = None
        try:
            query = self._session_cm.session.query(Episode).filter(
                Episode._id == episode_id)
            episode = query.one()
        except NoResultFound:
            print(f'Episode {episode_id} was not found')

        return episode

    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.merge(episode)
            scm.commit()

    def add_multiple_episodes(self, episode: List[Episode]):
        with self._session_cm as scm:
            for episode in episode:
                scm.session.merge(episode)
            scm.commit()

    def get_number_of_episodes(self) -> int:
        num_episodes = self._session_cm.session.query(Episode).count()
        return num_episodes

    def get_episodes_for_podcast(self, podcast_id: int) -> List[Episode]:
        """Get all episodes for a specific podcast by podcast_id."""
        with self._session_cm as scm:
            episodes = scm.session.query(Episode).filter(
                Episode._podcast_id == podcast_id).all()
            return episodes
    def get_number_of_episodes_for_podcast(self, podcast_id: int) -> int:
        """ Returns the number of episodes for a particular podcast by podcast_id. """
        count = 0
        try:
            count = self._session_cm.session.query(func.count(Episode._Episode__id)).join(
                Episode._Episode__podcast).filter(Podcast._id == podcast_id).scalar()
        except NoResultFound:
            print(f'No episodes found for Podcast {podcast_id}')

        return count

    # endregion

    def search_podcast_by_title(self, title_string: str) -> List[Podcast]:

        with self._session_cm as scm:
            podcasts = scm.session.query(Podcast).filter(
                Podcast._title.ilike(f'%{title_string.strip()}%')).all()
        return podcasts

    def search_podcast_by_author(self, author_name: str) -> List[Podcast]:
        with self._session_cm as scm:
            podcasts = scm.session.query(Podcast).join(Author).filter(
                Author._name.ilike(f'%{author_name}%')).all()
            return podcasts

    def search_podcast_by_category(self, category_string: str) -> List[Podcast]:
        with self._session_cm as scm:
            podcasts = scm.session.query(Podcast).join(Podcast.categories).filter(
                Category._name.ilike(f'%{category_string}%')).all()
        return podcasts

    def search_podcast_by_language(self, language_string: str) -> List[Podcast]:
        with self._session_cm as scm:
            podcasts = scm.session.query(Podcast).filter(
                Podcast._language.ilike(f'%{language_string}%')).all()
            return podcasts

    # stuff from mem_repo
    def set_podcasts(self, podcast: Podcast):
        pass

    def get_list_of_podcasts_titles(self) -> List[str]:
        pass

    def get_podcasts_by_alphabet(self, list_of_names):
        podcasts = self._session_cm.session.query(Podcast).order_by(Podcast._title.asc()).all()

        def custom_sort_key(podcast):
            title = podcast.title
            if title[0].isalpha():
                return 0, title.lower()
            else:
                return 1, title.lower()

        podcasts = sorted(podcasts, key=custom_sort_key)
        return podcasts

    def get_category(self, category_name) -> Category:
        with self._session_cm as scm:
            category = scm.session.query(Category).filter(Category._name == category_name).one_or_none()
            return category

    def add_episodes(self, episode: Episode):
        pass

    def get_podcasts_by_id(self) -> List['Podcast']:
        podcasts = self._session_cm.session.query(Podcast).order_by(Podcast._id.asc()).all()
        return podcasts

    def update_users_playlist(self, playlist: Playlist):
        try:
            existing_playlist = self._session_cm.session.query(Playlist).filter(Playlist._id == playlist.id).one_or_none()
            if existing_playlist:
                existing_playlist._episodes = playlist.list_of_episodes

            else:
                pass
            self._session_cm.session.commit()
        except Exception as e:
            self._session_cm.session.rollback()
            raise e

    def get_reviews(self) -> List[Review]:
        return self._session_cm.session.query(Review).all()

    def get_reviews_for_podcast(self, podcast_id: int) -> List[Review]:
        with self._session_cm as scm:
            # Join the Review table with the Podcast table and filter based on Podcast._id
            podcast_reviews = scm.session.query(Review).join(Review._podcast).filter(Podcast._id == podcast_id).all()
            return podcast_reviews


    def get_random_podcasts(self) -> List[Podcast]:
        podcasts = self._session_cm.session.query(Podcast).order_by(func.random()).limit(10).all()
        return podcasts

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._username == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def get_playlist_by_user(self, user: User) -> Playlist:
        playlist = self._session_cm.session.query(Playlist).filter(Playlist._user == user).first()
        return playlist

    def add_playlist(self, playlist: Playlist):
        with self._session_cm as scm:
            scm.session.merge(playlist)
            scm.commit()

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_episodes_by_date(self, episodes: List[Episode]) -> List[Episode]:
        pass