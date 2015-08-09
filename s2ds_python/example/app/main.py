"""Main.py

The main API for the project.
"""

import logging
import requests
import sqlalchemy.orm as orm

import app.helpers.db as db
import app.models.webdata as webdata
import app.settings as settings
import app.fetch

engine = db.create_engine(settings.HOST, settings.SCHEMA)
logging.basicConfig(filename="example.log", level=logging.DEBUG)
logger = logging.getLogger("example")

def create():
    """Create all schema tables."""

    logger.info("creating tables")
    res = webdata.Base.metadata.create_all(engine)

def fetch(url):
    """Create the application and session.

    Args:
        url (str): The URL to fetch and store
    """

    logger.info("setting up application session")
    Session = orm.sessionmaker(bind=engine)
    session = Session()

    data = app.fetch.fetch(url)
    q = session.query(webdata.WebData)
