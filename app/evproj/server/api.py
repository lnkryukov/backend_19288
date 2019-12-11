from .. import cfg
from ..db import *
from . import auth
from .exceptions import NotJsonError, NoData
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from . import util
from datetime import datetime
import requests
import logging
import os


def register_user(login, mail, name, surname, password, lvl=2):
    with get_session() as s:
        user_login = s.query(User).filter(
                User.login == login,
                User.status == 'deleted',
        ).one_or_none()
        user_mail = s.query(User).filter(
                User.mail == mail,
                User.status == 'deleted',
        ).one_or_none()
        if user_login or user_mail:
            user.status = 'unconfirmed'
            user.lvl = lvl
        else:
            confirmation_link = util.random_string_digits(25)
            user = User(login=login, mail=mail, name=name,
                        surname=surname, password=password,
                        lvl=lvl, confirmation_link=confirmation_link)
            s.add(user)
        logging.info('Registering new user [{}]'.format(login))


def get_events():
    result = {}
    with get_session() as s:
        events = s.query(Event).all()

        for event in events:
            result[event.id] = {
                'id': event.id,
                'name': event.name,
                'creator': event.creator,
                'date': event.date_time,
            }
    return result


def create_event(name, creator, date_time):
    timedate = date_time.split('-')
    time_date = datetime(int(timedate[0]), int(timedate[1]), int(timedate[2]),
                         int(timedate[3]), int(timedate[4]), 0, 0)
    with get_session() as s:
        user_id = s.query(User).filter(
                User.login == creator,
        ).one_or_none().id

        event = Event(name=name, creator=user_id, date_time=time_date)
        s.add(event)
        logging.info('Creating new event [{}]'.format(name))


def get_event_info(id):
    with get_session() as s:
        event = s.query(Event).filter(
                Event.id == id,
        ).one_or_none()

        return event


def confirm_user(confirmation_link):
    with get_session() as s:
        user = s.query(User).filter(
                User.confirmation_link == confirmation_link,
                User.status == 'unconfirmed',
        ).one_or_none()
        if user:
            user.status = 'active'
