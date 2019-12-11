from sqlalchemy import (Column, Integer, String, ForeignKey,
                        DateTime, Boolean, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM, UUID
from flask_login import UserMixin

from datetime import datetime
import uuid


Base = declarative_base()


Status = ENUM('active', 'deleted', name='status')
User_status = ENUM('unconfirmed', 'active', 'deleted', 'banned', name='user_status')
Event_status = ENUM('unconfirmed', 'future', 'past', name='event_status')


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    mail = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    cookie_id = Column(UUID(as_uuid=True), default=uuid.uuid4,
                       unique=True, nullable=False)
    lvl = Column(Integer, default=2, nullable=False)
    status = Column(User_status, default='active', nullable=False)
    confirmation_link = Column(String, nullable=False)

    def get_id(self):
        return self.cookie_id


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    creator = Column(Integer, ForeignKey('users.id'), nullable=False)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_time = Column(DateTime, nullable=False)
    event_status = Column(Event_status, default='unconfirmed', nullable=False)
    registration_status = Column(Boolean, default=True, nullable=False)
