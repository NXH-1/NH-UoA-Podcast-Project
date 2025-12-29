"""Initialize Flask app."""
import os

from typing import Iterable

from flask import Flask, render_template, request
from pathlib import Path

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import podcast.adapters.repository as repo
from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.adapters.repository_populate import populate
from podcast.adapters.orm import mapper_registry, map_model_to_tables


from podcast.adapters.memory_repository import MemoryRepository
from podcast.domainmodel.model import User


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file
    app.config.from_object('config.Config')
    data_path = 'podcast/adapters/'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # for mem repo
        repo.repo_instance = MemoryRepository()
        database_mode = False
        populate(data_path, repo.repo_instance, database_mode)

    elif app.config['REPOSITORY'] == 'database':
        # SQLALCHEMY DB
        database_uri = 'sqlite:///podcasts.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        app.config['SQLALCHEMY_ECHO'] = True  # echo SQL statements - useful for debugging

        # Create a database engine and connect it to the specified database
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=False)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = SqlAlchemyRepository(session_factory)

        if len(inspect(database_engine).get_table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            # Conditionally create database tables.
            mapper_registry.metadata.create_all(database_engine)
            # Remove any data from the tables.
            for table in reversed(mapper_registry.metadata.sorted_tables):
                with database_engine.connect() as conn:
                    conn.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            populate(data_path, repo.repo_instance, database_mode)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .description import description
        app.register_blueprint(description.description_bp)

        from .podcasts import podcasts
        app.register_blueprint(podcasts.podcasts_bp)

        from .search import search
        app.register_blueprint(search.search_bp)

        # register authentication blueprint
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        # register playlist blueprint
        from .playlist import playlist
        app.register_blueprint(playlist.playlist_bp)

    return app
