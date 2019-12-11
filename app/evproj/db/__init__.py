from .. import cfg
from .models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging


_engine = create_engine(cfg.DB_CONNECTION_STRING)
_Session = sessionmaker(bind=_engine, expire_on_commit=False)


@contextmanager
def get_session():
    session = _Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def create_tables(password):
    logging.info('Dropping existing tables')
    for tbl in reversed(Base.metadata.sorted_tables):
        try:
            tbl.drop(_engine)
        except:
            pass
    logging.info('Creating tables')
    Base.metadata.create_all(_engine)
    logging.info('Tables was created')
    with get_session() as s:
        root = User(
            login='root_admin',
            password=password,
            mail='root_admin_mail',
            name='Name',
            surname='Surname',
            lvl=0,
            status='active',
            confirmation_link='none',
        )
        s.add(root)
    logging.info('Default user [root_admin] was created')


#def upgrade_schema():
    #logging.info('Upgrading tables schema')
    #from .models import Tokens as tb
    #tb.__table__.create(_engine)
