from sqlalchemy import (Column, Integer, String, ForeignKey,
                        DateTime, Boolean, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM, UUID, TEXT
from flask_login import UserMixin

from datetime import datetime
import uuid

from .. import cfg


Base = declarative_base()


Status = ENUM('active', 'deleted',
              name='status')
User_status = ENUM('unconfirmed', 'active', 'deleted', 'banned',
                   name='user_status')
Participation_role = ENUM('creator', 'manager', 'presenter', 'participant',
                           name='participation_role')


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    mail = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(TEXT, nullable=False)
    phone = Column(String, nullable=True)
    cookie_id = Column(UUID(as_uuid=True), default=uuid.uuid4,
                       unique=True, nullable=False)
    lvl = Column(Integer, default=2, nullable=False)
    status = Column(User_status, default=cfg.DEFAULT_USER_STATUS, nullable=False)
    confirmation_link = Column(String, nullable=False)

    def get_id(self):
        return self.cookie_id


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    issued = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(Status, default='active', nullable=False)


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sm_description = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)


class Participation(Base):
    __tablename__ = 'participations'

    id = Column(Integer, primary_key=True)
    event = Column(Integer, ForeignKey('events.id'), nullable=False)
    participant = Column(Integer, ForeignKey('users.id'), nullable=False)
    participation_role = Column(Participation_role, default='participant', nullable=False)
