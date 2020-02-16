from sqlalchemy import (Column, Integer, String, ForeignKey,
                        DateTime, Boolean, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM, UUID, TEXT
from flask_login import UserMixin

from datetime import datetime
import uuid

from ..config import cfg


Base = declarative_base()


Status = ENUM('active', 'deleted',
              name='status')
User_status = ENUM('unconfirmed', 'active', 'deleted', 'banned',
                   name='user_status')
Participation_role = ENUM('creator', 'manager', 'presenter', 'participant',
                           name='participation_role')
Service_status = ENUM('admin', 'moderator', 'user', name='participation_role')


class User(Base, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    account_status = Column(User_status, default=cfg.DEFAULT_USER_STATUS,
                            nullable=False)
    confirmation_link = Column(String, nullable=False)
    cookie_id = Column(UUID(as_uuid=True), default=uuid.uuid4,
                       unique=True, nullable=False)
    # primary info
    mail = Column(String, unique=True, nullable=False)
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

    def change_password(self, old_password, new_password):
        opw = str(old_password).encode('utf-8')
        pw = str(self.password).encode('utf-8')
        if bcrypt.checkpw(opw, pw):
            npw = bcrypt.hashpw(str(new_password).encode('utf-8'),
                               bcrypt.gensalt())
            self.password = npw.decode('utf-8')
            return 1
        else:
            return 0


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sm_description = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    start_time = Column(DateTime, nullable=True)

    location = Column(String, nullable=False)
    site_link = Column(String, nullable=False)
    additional_info = Column(TEXT, nullable=False)


class Participation(Base):
    __tablename__ = 'participations'

    id = Column(Integer, primary_key=True)
    event = Column(Integer, ForeignKey('events.id'), nullable=False)
    participant = Column(Integer, ForeignKey('users.id'), nullable=False)
    participation_role = Column(Participation_role, default='participant', nullable=False)
