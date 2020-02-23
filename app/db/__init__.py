from .models import *
from ..config import cfg
from .. import logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


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
    logger.info('Dropping existing tables')
    try:
        Base.metadata.reflect(_engine)
        Base.metadata.drop_all(_engine)
    except Exception as e:
        logger.info('Failed to drop tables.\n{}'.format(str(e)))
    logger.info('Creating tables')
    Base.metadata.create_all(_engine)
    logger.info('Tables was created')
    with get_session() as s:
        root = User(
            mail='root_mail',
            password=password,
            name='Name',
            surname='Surname',
            service_status='admin',
            account_status='active',
            confirmation_link='none',
        )
        s.add(root)
    logger.info('Default user with mail [root_mail] was created')
