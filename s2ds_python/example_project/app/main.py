import requests
import sqlalchemy.orm as orm

import app.helpers.db as db
import app.models.webdata as webdata

engine = db.create_engine('localhost', 'training')

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