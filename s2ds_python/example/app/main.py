import requests
import sqlalchemy.orm as orm

import app.helpers.db as db
import app.models.webdata as webdata
import app.settings as settings

engine = db.create_engine(settings.HOST, settings.SCHEMA)

def create():
    """Create all schema tables."""

    print "creating tables"
    res = webdata.Base.metadata.create_all(engine)

def fetch(url):
    """Create the application and session."""

    print "setting up application session"
    Session = orm.sessionmaker(bind=engine)
    session = Session()
    q = session.query(webdata.WebData)
    print q.all()
