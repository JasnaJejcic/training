import requests
import sqlalchemy.orm as orm

import example.app.helpers.db as db
import example.app.models.webdata as webdata
import example.app.settings as settings

engine = db.create_engine(settings.HOST, settings.schema)

def create_tables():
    """Create all schema tables."""

    print "creating tables"
    res = webdata.Base.metadata.create_all(engine)

def create_app():
    """Create the application and session."""

    print "setting up application session"
    Session = orm.sessionmaker(bind=engine)
    session = Session()
    q = session.query(webdata.WebData)
    print q.all()
