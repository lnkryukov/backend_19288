from sqlalchemy import (Column, Integer, String, ForeignKey,
                        DateTime, Date, Time, Boolean, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM, UUID, TEXT
from flask_login import UserMixin

from datetime import datetime
import uuid

from ..config import cfg


Base = declarative_base()


Account_status = ENUM('unconfirmed', 'active', 'deleted', 'banned',
                   name='account_status')
Participation_role = ENUM('creator', 'manager', 'presenter', 'viewer',
                           name='participation_role')
Service_status = ENUM('superadmin', 'admin', 'moderator', 'user', name='service_status')


class User(Base, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    account_status = Column(Account_status, default=cfg.DEFAULT_USER_STATUS,
                            nullable=False)
    confirmation_link = Column(String, nullable=False)
    cookie_id = Column(UUID(as_uuid=True), default=uuid.uuid4,
                       unique=True, nullable=False)
    # primary info
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(TEXT, nullable=False)
    service_status = Column(Service_status, default='user', nullable=False)
    # secondary info
    phone = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    position = Column(String, nullable=True)
    country = Column(String, nullable=True)

    # био можно отредактировать при регистрации в качестве спикера
    bio = Column(TEXT, nullable=True)

    def get_id(self):
        return self.cookie_id


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sm_description = Column(String, nullable=False)
    description = Column(String, nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    start_time = Column(Time, nullable=True)

    location = Column(String, nullable=False)
    site_link = Column(String, nullable=False)
    additional_info = Column(TEXT, nullable=False)


class Participation(Base):
    __tablename__ = 'participations'

    id = Column(Integer, primary_key=True)
    e_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    u_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    participation_role = Column(Participation_role, default='viewer', nullable=False)
    report = Column(TEXT, nullable=True)
    presenter_description = Column(TEXT, nullable=True)
