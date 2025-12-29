from typing import List, Iterable

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Author, Episode, Category


class NonExistentPodcastException(Exception):
    pass


def get_random_podcasts(repo: AbstractRepository):
    podcasts = repo.get_random_podcasts()
    return podcasts_to_dict(podcasts)


def podcast_to_dict(podcast: Podcast):
    categories = categories_to_string(podcast.categories)

    podcast_dict = {
        'id': podcast.id,
        'author': podcast.author.name,
        'title': podcast.title,
        'image': podcast.image,
        'description': podcast.description,
        'website': podcast.website,
        'itunes_id': podcast.itunes_id,
        'language': podcast.language,
        'categories': categories,

    }
    return podcast_dict


def podcasts_to_dict(podcasts: Iterable[Podcast]):
    return [podcast_to_dict(podcast) for podcast in podcasts]


def categories_to_string(categories: List[Category]) -> str:
    categories_str = []
    for category in categories:
        categories_str.append(category.name)
    return " | ".join(categories_str)


def get_list_of_podcasts_titles(repo: AbstractRepository) -> List[str]:
    return [podcast.title for podcast in repo.get_podcasts()]
