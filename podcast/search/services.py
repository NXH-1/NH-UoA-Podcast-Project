from typing import List, Iterable

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Author, Episode, Category


def search_results(repo: AbstractRepository, query: str, filter_by: str):
    results = []
    if filter_by == 'title':
        results = repo.search_podcast_by_title(query)
    elif filter_by == 'author':
        results = repo.search_podcast_by_author(query)
    elif filter_by == 'category':
        results = repo.search_podcast_by_category(query)
    elif filter_by == 'language':
        results = repo.search_podcast_by_language(query)

    return sort_search(results)


def sort_search(podcasts: List[Podcast]):
    def custom_sort_key(podcast):
        title = podcast.title
        if title[0].isalpha():
            return 0, title.lower()
        else:
            return 1, title.lower()

    sorted_podcasts = sorted(podcasts, key=custom_sort_key)
    return sorted_podcasts


def pagination(page: int, podcasts: List[Podcast]):
    per_page = 8
    start = (page - 1) * per_page
    end = start + per_page
    total = (len(podcasts) + per_page - 1) // per_page
    return podcasts[start:end], total
