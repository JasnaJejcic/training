import sqlalchemy as sqla
import os.path

def create_engine(host, db_name=None):
    """Create DB engine.

    Args:
        host: Name of the host e.g. localhost
        db_name: Database name

    Returns:
        engine
    """

    url = sqla.engine.url.URL(
                drivername='mysql',
                host=host,
                database=db_name,
                query={
                    'read_default_file': os.path.expanduser('~') + '/.my.cnf',
                    'charset': 'utf8'
                }
    )

    connect_args = {}
    engine = sqla.create_engine(name_or_url=url,
                           pool_recycle=300,
                           pool_size=10,
                           connect_args=connect_args)
    return engine
