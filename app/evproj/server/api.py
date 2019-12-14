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


def register_user(mail, name, surname, password, lvl=2):
    with get_session() as s:
        user = s.query(User).filter(
                User.mail == mail,
                User.status == 'deleted',
        ).one_or_none()
        if user:
            user.status = 'unconfirmed'
            user.lvl = lvl
        else:
            confirmation_link = util.random_string_digits(25)
            user = User(mail=mail, name=name,
                        surname=surname, password=password,
                        lvl=lvl, confirmation_link=confirmation_link)
            s.add(user)
        logging.info('Registering new user [{}]'.format(mail))


def get_events():
    result = {}
    with get_session() as s:
        events = s.query(Event).all()

        for event in events:
            result[event.id] = {
                'id': event.id,
                'name': event.name,
                'sm_description': event.sm_description,
                'date': event.date_time,
            }
    return result


def create_event(name, sm_description, description, date_time, phone, mail):
    timedate = date_time.split('-')
    time_date = datetime(int(timedate[0]), int(timedate[1]), int(timedate[2]),
                         int(timedate[3]), int(timedate[4]), 0, 0)
    with get_session() as s:
        last_event = s.query(Event).order_by(Event.id.desc()).first()
        event = Event(name=name, sm_description=sm_description, description=description,
                        date_time=time_date, phone=phone, mail=mail)
        s.add(event)
        logging.info('Creating new event [{}]'.format(name))
        if last_event:
            return last_event.id + 1
        else:
            return 1


def create_event_creator(creator, last_id):
    with get_session() as s:
        participation = Participation(event=last_id, participant=creator,
                                        participation_level='creator', participation_status='confirmed')
        s.add(participation)
        logging.info('Added creator [{}] to event id [{}]'.format(creator, last_id))


def get_event_info(id):
    with get_session() as s:
        event = s.query(Event).filter(
                Event.id == id,
        ).one_or_none()

        return event


def check_participation(user_id, event_id):
    with get_session() as s:
        participation = s.query(Participation).filter(
                Participation.event == event_id,
                Participation.participant == user_id
        ).one_or_none()
        if participation:
            return participation.participation_level
        else:
            return 'not joined'


def get_participators(id):
    result = {}
    with get_session() as s:
        users = s.query(User, Event, Participation).filter(
                User.id == Participation.participant,
                Event.id == Participation.event,
                Event.id == id
        ).all()

        for user, _, participant in users:
            if participant.participation_level is not 'guest':
                result[user.id] = {
                    'name': user.name,
                    'surname': user.surname,
                    'participation_level': participant.participation_level,
                }

    return result


def get_stat(event_id):
    with get_session() as s:
        confirmed_users = s.query(Participation).filter(
                Participation.event == event_id,
                Participation.participation_level == 'guest',
                Participation.participation_status == 'confirmed'
        ).count()

        unconfirmed_users = s.query(Participation).filter(
                Participation.event == event_id,
                Participation.participation_level == 'guest',
                Participation.participation_status == 'declined'
        ).count()

        return confirmed_users, unconfirmed_users


def guest_join(user_id, event_id):
    with get_session() as s:
        participation = Participation(event=event_id, participant=user_id,
                                        participation_level='guest', participation_status='unknown')
        s.add(participation)


def guest_confirm(user_id, event_id, action):
    with get_session() as s:
        part = s.query(Participation).filter(
            Participation.event == event_id,
            Participation.participant == user_id,
            Participation.participation_status == 'unknown'
        ).first()
        setattr(part, 'participation_status', action)
        s.commit()


def get_uncorfimed_users(event_id):
    result = {}
    with get_session() as s:
        users = s.query(User, Participation).filter(
                User.id == Participation.participant,
                Participation.event == event_id,
                Participation.participation_status == 'unknown'
        ).all()

        for user, _ in users:
            result[user.id] = {
                'id': user.id,
                'name': user.name,
                'surname': user.surname,
            }

    return result


def event_exist(event_id):
    with get_session() as s:
        exists = s.query(Event).filter(
                Event.id == event_id
        ).count()
    return True if exists > 0 else False


def confirm_user(confirmation_link):
    with get_session() as s:
        user = s.query(User).filter(
                User.confirmation_link == confirmation_link,
                User.status == 'unconfirmed',
        ).one_or_none()
        if user:
            user.status = 'active'
