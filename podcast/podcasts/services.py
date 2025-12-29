from typing import List, Iterable

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Author, Episode, Category, Review


class NonExistentPodcastException(Exception):
    pass


def get_podcasts_by_alphabet(list_of_titles: List[str], repo: AbstractRepository):
    podcasts = repo.get_podcasts_by_alphabet(list_of_titles)

    return podcasts_to_dict(podcasts)


def podcast_to_dict(podcast: Podcast):
    # maybe make this into a method
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


def pagination(page: int, podcasts: List[Podcast]):
    per_page = 12
    start = (page - 1) * per_page
    end = start + per_page
    total = (len(podcasts) + per_page - 1) // per_page
    return podcasts[start:end], total
