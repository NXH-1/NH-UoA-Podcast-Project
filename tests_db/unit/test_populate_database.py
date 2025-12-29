from sqlalchemy import select, inspect

from podcast.adapters.orm import mapper_registry
from tests_db.conftest import database_engine


def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors',
                                           'categories',
                                           'episodes',
                                           'playlist_episodes',
                                           'playlists',
                                           'podcast_categories',
                                           'podcasts',
                                           'reviews',
                                           'users']
    # Checked that we have all the tables made


def test_database_populate_select_all_categories(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_categories_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table tags
        categories_table = mapper_registry.metadata.tables[name_of_categories_table]
        select_statement = select(categories_table)
        result = connection.execute(select_statement).mappings()  # Get dictionary-like interface for the rows

        all_categories_names = []
        # Goes through the rows in the table and append the necessary column info
        for row in result:
            all_categories_names.append(row['category_name'])

        assert all_categories_names == ['Society & Culture',
                                        'Personal Journals',
                                        'Professional',
                                        'News & Politics',
                                        'Sports & Recreation',
                                        'Comedy',
                                        'Religion & Spirituality',
                                        'Christianity',
                                        'Amateur',
                                        'Government & Organizations',
                                        'Natural Sciences',
                                        'Science & Medicine',
                                        'National',
                                        'Business']
    # Check that categories are all here when referring to the test CSV files


def test_database_populate_select_all_authors(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table authors
        authors_table = mapper_registry.metadata.tables[name_of_authors_table]
        select_statement = select(authors_table)
        result = connection.execute(select_statement).mappings()  # Get dictionary-like interface for the rows

        all_authors_names = []
        # Goes through the rows in the table and append the necessary column info
        for row in result:
            all_authors_names.append(row['name'])

        assert all_authors_names == ['D Hour Radio Network',
                                     'Brian Denny',
                                     'Radio Popolare',
                                     'Tallin Country Church',
                                     'Eric Toohey',
                                     'msafoschnik',
                                     'Janelle Vecchio and Phil Vecchio',
                                     'Audioboom',
                                     'Unknown author']
        # Check that all authors in test CSV file is populated


def test_database_populate_select_all_episodes(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_episodes_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table episodes
        episodes_table = mapper_registry.metadata.tables[name_of_episodes_table]
        select_statement = select(episodes_table)
        result = connection.execute(select_statement).mappings()  # Get dictionary-like interface for the rows

        all_episodes_titles = []
        # Goes through the rows in the table and append the necessary column info
        for row in result:
            all_episodes_titles.append(row['title'])

        assert all_episodes_titles == ['The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass '
                                       'Challenge Part 3',
                                       'TRUMPMANIA - Lavie Margolin talks about his book',
                                       'Waiting',
                                       'Prepare For The Lord',
                                       'The Mandarian Orange Show Episode 75- The Luggage Gamble, or: 30 Day '
                                       'MoviePass Challenge Part 4',
                                       '1: Festive food and farming',
                                       'Onde Road di dom 03/12',
                                       'Believing the Impossible (Luke 1:26-45)',
                                       "God's Certain Word (Luke 1:1-25)",
                                       'Onde Road di dom 31/12',
                                       'LOCKED ON CUBS - 12/27/17 - Waiting on Yu',
                                       'LOCKED ON CUBS - 12/18/2017 - Episode 4: Is Yu Darvish a New Hope for the '
                                       'offseason?',
                                       'LOCKED ON CUBS - 12/15/2017 - Fighting off the Cardinals and Alex Cobb '
                                       'concerns',
                                       'Dean Ep5: Two Legged Foxes',
                                       'Say It! Radio',
                                       'Tallin Service for 12 03 2017',
                                       'John 20:31 Christmas Practice song',
                                       'Say It! Radio',
                                       'Say It! Radio...Alter Ego Friday',
                                       'Tallin Service for 12 17 2017']
    # Check that all episodes from test CSV file is populated properly


def test_database_populate_select_all_podcasts(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_podcasts_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table podcasts
        podcasts_table = mapper_registry.metadata.tables[name_of_podcasts_table]
        select_statement = select(podcasts_table)
        result = connection.execute(select_statement).mappings()  # Get dictionary-like interface for the rows

        # Goes through the rows in the table and append the necessary column info
        all_podcasts_titles = []
        for row in result:
            all_podcasts_titles.append(row['title'])

        assert all_podcasts_titles == ['D-Hour Radio Network',
                                       'Brian Denny Radio',
                                       'Onde Road - Radio Popolare',
                                       'Tallin Messages',
                                       'Bethel Presbyterian Church (EPC) Sermons',
                                       'Mike Safo',
                                       'The Mandarian Orange Show',
                                       'Crawlspace: True Crime & Mysteries',
                                       'AHDB',
                                       'Locked on Cubs',
                                       'Montvale Evangelical Free Church Podcast']
        # Check that all podcasts from test CSV file is populated properly


def test_database_populate_select_all_podcast_categories_association(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_podcast_categories_association_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table podcast_categories_association
        podcast_categories_association_table = mapper_registry.metadata.tables[
            name_of_podcast_categories_association_table]
        select_statement = select(podcast_categories_association_table)
        result = connection.execute(select_statement).mappings()  # Get dictionary-like interface for the rows

        all_associations = []
        # Goes through the rows in the table and append the necessary column info
        for row in result:
            all_associations.append((row['podcast_id'], row['category_id']))  # append it as tuple

        # This is all the correct association:
        correct_assoc = [(281, 7),
                         (281, 8),
                         (4, 7),
                         (5, 7),
                         (5, 8),
                         (2, 3),
                         (2, 4),
                         (2, 5),
                         (2, 6),
                         (6, 5),
                         (6, 9),
                         (1, 1),
                         (1, 2),
                         (3, 1),
                         (100, 10),
                         (100, 11),
                         (100, 12),
                         (100, 13),
                         (100, 14),
                         (14, 6),
                         (177, 5),
                         (23, 2),
                         (23, 1),
                         (23, 4)]

    # goes through all tuples and check that it is part of the correct associations
        for assoc in all_associations:
            assert assoc in correct_assoc
    # Check that the association between podcast and categories and populated correctly


