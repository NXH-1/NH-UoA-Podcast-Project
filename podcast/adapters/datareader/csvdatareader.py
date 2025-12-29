import os
import csv
from podcast.domainmodel.model import Podcast, Episode, Author, Category


class CSVDataReader:
    def __init__(self, episode_file_path: str, podcast_file_path: str):
        self.episode_file_path = episode_file_path
        self.podcast_file_path = podcast_file_path
        self.__dataset_of_podcasts = []
        self.__dataset_of_episodes = []
        self.__dataset_of_authors = set()
        self.__dataset_of_categories = set()

    @property
    def __episode_path__(self) -> str:
        return self.episode_file_path

    @property
    def __podcast_path__(self) -> str:
        return self.podcast_file_path

    @property
    def dataset_of_podcasts(self) -> list:
        return self.__dataset_of_podcasts

    @property
    def dataset_of_episodes(self) -> list:
        return self.__dataset_of_episodes

    @property
    def dataset_of_authors(self) -> set:
        return self.__dataset_of_authors

    @property
    def dataset_of_categories(self) -> set:
        return self.__dataset_of_categories

    def read_episodes(self):
        podcast_lookup = {p.id: p for p in self.__dataset_of_podcasts}
        with open(self.episode_file_path, mode='r', newline='', encoding='utf-8') as csvepisodefile:
            reader = csv.DictReader(csvepisodefile)
            for row in reader:
                podcast_id =int(row['podcast_id'])
                podcast = podcast_lookup.get(podcast_id)
                if podcast is not None:
                    new_episode = Episode(
                        episode_id=int(row['id']),
                        podcast_id=podcast_id,
                        title=row['title'],
                        episode_link=row['audio'],
                        episode_length=int(row['audio_length']),
                        episode_description=row['description'],
                        pub_date=row['pub_date']
                    )
                if Episode not in self.__dataset_of_episodes:
                    podcast.add_episode(new_episode)
                    self.__dataset_of_episodes.append(new_episode)

    def read_podcasts(self):
        with open(self.podcast_file_path, mode='r', newline='', encoding='utf-8') as podcast_file:
            podcasts_rows = csv.DictReader(podcast_file)
            author_count = 1
            category_count = 1
            for row in podcasts_rows:
                author_name = row['author']
                if author_name == '':
                    author_name = 'Unknown author'
                if (author_name == 'Unknown author') and 'Unknown author' in [author.name for author in self.__dataset_of_authors]:
                    for a in self.__dataset_of_authors:
                        if a.name == 'Unknown author':
                            author = a
                else:
                    author = Author(author_count, author_name)
                    if author.name not in [a.name for a in self.__dataset_of_authors]:
                        author_count += 1
                        self.__dataset_of_authors.add(author)
                    else:
                        # Retrieve the existing author from the set to associate with the podcast
                        for existing_author in self.__dataset_of_authors:
                            if existing_author.name == author.name:
                                author = existing_author
                                break
                podcast = Podcast(
                    podcast_id=int(row['id']),
                    author=author,
                    title=row['title'],
                    image=row['image'],
                    description=row['description'],
                    website=row['website'],
                    itunes_id=int(row['itunes_id']),
                    language=row['language'],
                )
                category_names = row["categories"].split("|")
                for category_name in category_names:
                    category = Category(category_count, category_name.strip())
                    if category.name not in [c.name for c in self.__dataset_of_categories]:
                        self.__dataset_of_categories.add(category)
                        category_count += 1
                    else:
                        # Retrieve the existing category from the set to associate with the podcast
                        for existing_category in self.__dataset_of_categories:
                            if existing_category.name == category.name:
                                category = existing_category
                                break
                    podcast.add_category(category)
                self.__dataset_of_podcasts.append(podcast)