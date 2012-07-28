from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import config

user, password, host, database = config.get('database', 'user'), config.get('database', 'pw'), config.get('database', 'host'), config.get('database', 'database')

engine = create_engine('mysql://' + user + ':' + password + '@' + host + '/' + database, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import euskalmap.models
    Base.metadata.create_all(bind=engine)

def db_unique(model, **kwargs):
    instance = db_session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
		instance = model(**kwargs)
		db_session.add(instance)
		db_session.commit()
		return instance