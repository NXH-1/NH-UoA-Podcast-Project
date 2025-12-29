from datetime import datetime
from typing import List, Iterable

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Author, Episode, Category, Playlist, Review


class NonExistentEpisode(Exception):
    pass


class NonExistentPodcast(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_episode_by_id(episode_id: int, repo: AbstractRepository):
    episode = repo.get_episode(episode_id)
    return episode


def get_user_playlists(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    playlist = repo.get_playlist_by_user(user)
    if playlist is None:
        playlist = Playlist(user.id, user, f"{username}'s playlist")
        repo.add_playlist(playlist)

    return playlist


def add_episode_to_playlist(playlist: Playlist, episode: Episode, repo: AbstractRepository):
    playlist.add_episode(episode)
    repo.update_users_playlist(playlist)


def remove_episode_from_playlist(playlist: Playlist, episode: Episode, repo: AbstractRepository):
    playlist.remove_episode(episode)
    repo.update_users_playlist(playlist)


def get_episodes(podcast_id, repo: AbstractRepository):
    podcast_episodes = repo.get_episodes_for_podcast(podcast_id)
    sorted_episodes = sorted(podcast_episodes, key=lambda episode: datetime.strptime(episode.pub_date + '00',
                                                                             '%Y-%m-%d %H:%M:%S%z'))
    return sorted_episodes


def get_podcast_by_id(podcast_id, repo: AbstractRepository):
    podcasts = repo.get_podcasts_by_id()
    podcasts = [podcast_to_dict(podcast) for podcast in podcasts]
    if podcast_id > len(podcasts):
        raise NonExistentPodcast
    return podcasts[podcast_id - 1]


def episode_to_dict(episode: Episode):
    episode_dict = {
        'id': episode.id,
        'podcast_id': episode.pod_id,
        'title': episode.title,
        'link': episode.link,
        'length': episode.length,
        'description': episode.description,
        'pub_date': episode.pub_date
    }
    return episode_dict


def podcast_to_dict(podcast: Podcast):

    podcast_dict = {
        'id': podcast.id,
        'author': podcast.author.name,
        'title': podcast.title,
        'image': podcast.image,
        'description': podcast.description,
        'website': podcast.website,
        'itunes_id': podcast.itunes_id,
        'language': podcast.language,
        'categories': categories_to_string(podcast.categories),
        'reviews': [review_to_dict(review) for review in podcast.reviews]

    }
    return podcast_dict


def review_to_dict(review: Review):
    review_dict = {
        'review_id': review.id,
        'review_user': review.reviewer,
        'review_podcast': review.podcast,
        'podcast_rating': review.rating,
        'review_content': review.comment,
        'review_time': review.timestamp
    }
    return review_dict


def categories_to_string(categories: List[Category]) -> str:
    categories_str = []
    for category in categories:
        categories_str.append(category.name)
    return " | ".join(categories_str)


def episodes_to_dict(episodes: Iterable[Episode]):
    return [episode_to_dict(episode) for episode in episodes]


def add_review_to_podcast(username: str, podcast_id: int, comment_text: str, rating: int, repo: AbstractRepository):
    podcast = repo.get_podcast(podcast_id)
    if podcast is None:
        raise NonExistentPodcast

    # Retrieve the user (assumed that the repo can fetch the user by username)
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create a new review
    review = Review(
        review_id=len(repo.get_reviews()) + 1,  # Assuming you're generating review IDs sequentially
        review_user=user,
        review_podcast=podcast,
        podcast_rating=rating,
        review_content=comment_text
    )

    review.time_to_current_timestamp()
    # Add review to repo and Add the review to the podcast
    repo.add_review(review)


def retrieve_podcast_reviews(podcast_id, repo: AbstractRepository):
    reviews = repo.get_reviews_for_podcast(podcast_id)
    return reviews


def get_average_podcast_rating(podcast_id, repo: AbstractRepository):
    podcast = repo.get_podcast(podcast_id)
    avg_rating = podcast.average_rating()
    avg = {
        'number': round(avg_rating, 1),
        'stars': round(avg_rating) * "★" + (5 - round(avg_rating)) * "☆"
    }
    return avg


def pagination(page: int, episodes: List):
    per_page = 6
    start = (page - 1) * per_page
    end = start + per_page
    total = (len(episodes) + per_page - 1) // per_page
    return episodes[start:end], total


def add_all_episodes_to_playlist(playlist: Playlist, podcast_id: int, repo: AbstractRepository):
    podcast_episodes = get_episodes(podcast_id, repo)

    if podcast_episodes:
        for episode in podcast_episodes:
            if episode not in playlist.list_of_episodes:
                playlist.add_episode(episode)
        repo.update_users_playlist(playlist)


def remove_all_episodes_from_playlist(playlist: Playlist, podcast_id: int, repo: AbstractRepository):
    podcast_episodes = get_episodes(podcast_id, repo)
    if podcast_episodes:
        for episode in podcast_episodes:
            if episode in playlist.list_of_episodes:
                playlist.remove_episode(episode)
        repo.update_users_playlist(playlist)