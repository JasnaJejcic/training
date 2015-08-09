import sqlalchemy as sqla
import sqlalchemy.ext.declarative as sql_dec

Base = sql_dec.declarative_base()

class WebData(Base):
    __tablename__ = "webdata"

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    url = sqla.Column(sqla.VARCHAR(255))
    data = sqla.Column(sqla.TEXT)

