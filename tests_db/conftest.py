from pathlib import Path

import pytest
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from podcast.adapters import database_repository, repository_populate
from podcast.adapters.orm import mapper_registry, map_model_to_tables


test_data_path = Path(__file__).parent / '..' / 'tests'

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///podcasts-test.db'


@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    mapper_registry.metadata.create_all(engine)  # Conditionally create database tables.
    with engine.connect() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):  # Remove any data from the tables.
            connection.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for a sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repository_populate.populate(test_data_path, repo_instance, database_mode)
    yield engine
    mapper_registry.metadata.drop_all(engine)


# Fixture Incomplete/untested
@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    mapper_registry.metadata.create_all(engine)
    with engine.connect() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):  # Remove any data from the tables.
            connection.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for a sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repository_populate.populate(test_data_path, repo_instance, database_mode)
    yield session_factory
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    mapper_registry.metadata.create_all(engine)
    connection = engine.connect()
    transaction = connection.begin()
    map_model_to_tables()
    session_factory = sessionmaker(bind=connection)
    session = session_factory()
    yield session
    session.close()
    transaction.rollback()
    connection.close()
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    clear_mappers()
    map_model_to_tables()
    mapper_registry.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    clear_mappers()
    session.close()