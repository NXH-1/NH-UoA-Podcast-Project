import os
import csv
from pathlib2 import Path
from podcast.adapters.repository import AbstractRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    episode_path = os.path.join(data_path, "data/episodes.csv")
    podcast_path = os.path.join(data_path, "data/podcasts.csv")

    reader = CSVDataReader(episode_path, podcast_path)

    reader.read_podcasts()
    reader.read_episodes()
    authors = reader.dataset_of_authors
    podcasts = reader.dataset_of_podcasts
    categories = reader.dataset_of_categories
    episodes = reader.dataset_of_episodes

    if database_mode:
        # Add authors to the repo
        repo.add_multiple_authors(authors)

        # Add categories to the repo
        repo.add_multiple_categories(categories)

        # # Add podcasts to the repo
        repo.add_multiple_podcasts(podcasts)

        # Add episodes to the repo
        repo.add_multiple_episodes(episodes)
    else:
        repo.set_podcasts(podcasts)
        repo.add_episodes(episodes)
        repo.add_multiple_authors(authors)
        repo.add_multiple_categories(categories)