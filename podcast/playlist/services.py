from typing import List, Iterable

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Playlist, Episode


class NonExistentEpisode(Exception):
    pass


def episode_podcast_dict(episode_list: List[Episode], repo: AbstractRepository) -> dict:
    ep_pod_dict = {}
    for episode in episode_list:
        ep_pod_dict[episode] = repo.get_podcast(episode.pod_id)
    return ep_pod_dict


def get_user_playlist(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    playlist = repo.get_playlist_by_user(user)
    if playlist is None:
        playlist = Playlist(user.id, user, f"{username}'s playlist")
        repo.add_playlist(playlist)
    return playlist


def get_episode_by_id(episode_id: int, repo: AbstractRepository):
    episode = repo.get_episode(episode_id)
    return episode


def remove_episode_from_playlist(playlist: Playlist, episode: Episode, repo: AbstractRepository):
    playlist.remove_episode(episode)
    repo.update_users_playlist(playlist)


def pagination(page: int, episodes: List):
    per_page = 9
    start = (page - 1) * per_page
    end = start + per_page

    total = (len(episodes) + per_page - 1) // per_page
    return episodes[start:end], total
