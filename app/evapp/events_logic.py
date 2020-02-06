from .config import cfg
from .db import *
from . import util
from .exceptions import NotJsonError, NoData

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

from datetime import datetime
import requests
import logging
import os
import nanoid


def get_events():
    result = {}
    with get_session() as s:
        events = s.query(Event).all()

        for event in events:
            result[event.id] = {
                'id': event.id,
                'name': event.name,
                'sm_description': event.sm_description,
                'date_time': event.date_time,
            }
    return result


def create_event(name, sm_description, description, date_time):
    timedate = date_time.split('T')
    c_date = timedate[0].split('-')
    c_time = timedate[1].split(':')
    time_date = datetime(int(c_date[0]), int(c_date[1]), int(c_date[2]),
                         int(c_time[0]), int(c_time[1]), 0, 0)
    with get_session() as s:
        last_event = s.query(Event).order_by(Event.id.desc()).first()
        event = Event(name=name, sm_description=sm_description,
                      description=description, date_time=time_date)
        s.add(event)
        logging.info('Creating event [{}] [{}]'.format(name, time_date))
        if last_event:
            return last_event.id + 1
        else:
            return 1


def create_event_creator(creator, last_id):
    with get_session() as s:
        participation = Participation(event=last_id, participant=creator,
                                      participation_role='creator')
        s.add(participation)


def check_participation(user_id, event_id):
    with get_session() as s:
        participation = s.query(Participation).filter(
                Participation.event == event_id,
                Participation.participant == user_id
        ).one_or_none()
        if participation:
            return participation.participation_role
        else:
            return 'not joined'


def get_presenters(id):
    result = {}
    with get_session() as s:
        users = s.query(User, Participation).filter(
                User.id == Participation.participant,
                Participation.event == id,
                Participation.participation_role == 'presenter' 
        ).all()

        i = 1
        for user, participant in users:
            result[i] = {
                'name': user.name,
                'surname': user.surname,
                'participation_role': participant.participation_role,
            }
            i += 1

    return result


def join_event(user_id, event_id, role):
    with get_session() as s:
        is_consists = s.query(Participation).filter(
                Participation.participant == user_id,
                Participation.event == event_id
        ).one_or_none()

        if not is_consists:
            participation = Participation(event=event_id, participant=user_id,
                                          participation_role=role)
            s.add(participation)
            logging.info('User [id {}] joined event [id {}] as [{}]'.format(user_id,
                                                                    event_id,
                                                                    role))
            return 0
        else:
            return 'User has already joined this event'


def event_exist(event_id):
    with get_session() as s:
        exists = s.query(Event).filter(
                Event.id == event_id
        ).count()
    return True if exists > 0 else False


def event_info(id):
    with get_session() as s:
        event = s.query(Event, Participation, User).filter(
                Event.id == id,
                Participation.event == Event.id,
                Participation.participant == User.id,
                Participation.participation_role == 'creator'
        ).first()

        return {
            "creator_mail": event.User.mail,
            "phone": event.User.phone,
            "name": event.Event.name,
            "sm_description": event.Event.sm_description,
            "description": event.Event.description,
            "date_time": event.Event.date_time
        }    







# TODO TODO




def update_event(user_id, event_id, params):
    with get_session() as s:
        event = s.query(Participation, Event).filter(
                Event.id == id,
                Participation.event == Event.id,
                Participation.participant == user_id,
                Participation.participation_role.in_(['creator', 'manager'])
        ).one_or_none()

        if event is None:
            return "You have no rights to edit this event"
        else:
            ev = event.Event

            try:
                print(ev['name'])
            except Exception as e:
                print(e)

            return "Updated successfully"
