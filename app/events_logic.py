from .config import cfg
from .db import *
from . import util
from . import logger
from .exceptions import (NotJsonError, NoData, WrongIdError, JoinUserError)

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, or_

from datetime import date, time
import requests
import os
import nanoid


def get_event_info(event_id):
    with get_session() as s:
        event = s.query(Event, Participation, User).filter(
                Event.id == event_id,
                Participation.event == Event.id,
                Participation.participant == User.id,
                Participation.participation_role == 'creator'
        ).first()

        if not event:
            raise WrongIdError('No event with this id')

        return {
            "creator_mail": event.User.mail,
            "phone": event.User.phone,
            "name": event.Event.name,
            "sm_description": event.Event.sm_description,
            "description": event.Event.description,
            "start_date": event.Event.start_date,
            "end_date": event.Event.end_date,
            "start_time": event.Event.start_time,
            "location": event.Event.location,
            "site_link": event.Event.site_link,
            "additional_info": event.Event.additional_info
        }


def get_events(offset, size):
    result = []
    with get_session() as s:
        events = s.query(Event).order_by(desc(Event.start_date))
        if offset and size:
            offset = int(offset)
            size = int(size)
            if offset < 0 or size < 1:
                raise WrongDataError('Offset or size has wrong values')
            events = events.slice(offset, offset+size)
        elif not offset and not size:
            events = events.all()
        else:
            raise KeyError('Wrong query string arg.')

        for event in events:
            result.append({
                'id': event.id,
                'name': event.name,
                'sm_description': event.sm_description,
                'start_date': event.start_date,
                'end_date': event.end_date,
                'start_time': event.start_time,
                'location': event.location,
                'site_link': event.site_link
            })
    return result


def create_event(user_id, data):
    start_date = data['start_date'].split('-')
    date_start = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))

    date_end = None
    start_time = None
    if 'end_date' in data.keys():
        end_date = data['end_date'].split('-')
        date_end = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
    if 'start_time' in data.keys():
        start_time = data['start_time'].split(':')
        time_start = time(int(start_time[0]), int(start_time[1]), 0, 0)
    
    with get_session() as s:
        event = Event(name=data['name'], sm_description=data['sm_description'],
                      description=data['description'], start_date=date_start,
                      end_date=date_end, start_time=time_start,
                      location=data['location'], site_link=data['site_link'],
                      additional_info=data['additional_info'])
        s.add(event)
        s.flush()
        s.refresh(event)
        participation = Participation(event=event.id, participant=user_id,
                                      participation_role='creator')

        logger.info('Creating event [{}] [{}] [{}] [{}]'.format(data['name'],
                                                                 date_start,
                                                                 date_end,
                                                                 start_time))
        return event.id


def update_event(user_id, event_id, data):
    with get_session() as s:
        event = s.query(Event).get(event_id)
        if not event:
            raise WrongIdError('No event with this id')
        


        for arg in data.keys():
            getattr(event, arg)
            if arg == 'start_date' or 'end_date':
                sdate = data[arg].split('-')
                date_start = date(int(sdate[0]), int(sdate[1]), int(sdate[2]))
                setattr(event, arg, date_start)
            elif arg == 'start_time':
                start_time = data[arg].split(':')
                time_start = time(int(start_time[0]), int(start_time[1]), 0, 0)
                setattr(event, arg, time_start)
            else:
                setattr(event, arg, data[arg])
            


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
    result = []
    with get_session() as s:
        event = s.query(Event).get(id)
        if not event:
            raise WrongIdError('No event with this id')
        users = s.query(User, Participation).filter(
                User.id == Participation.participant,
                Participation.event == id,
                Participation.participation_role == 'presenter' 
        ).all()

        for user, participant in users:
            result.append({
                'name': user.name,
                'surname': user.surname,
                'report': participant.report,
                'presenter_description': participant.presenter_description
            })

    return result


def join_event(user_id, event_id, data):
    with get_session() as s:
        event = s.query(Event).get(event_id)
        if not event:
            raise WrongIdError('No event with this id')

        is_consists = s.query(Participation).filter(
                Participation.participant == user_id,
                Participation.event == event_id
        ).one_or_none()

        if not is_consists:
            role = 'viewer'
            participation = Participation(event=event_id,
                                          participant=user_id,
                                          participation_role='viewer')
            if data['role'] == 'presenter':
                participation.participation_role = 'presenter'
                participation.report = data['report']
                participation.presenter_description = data['presenter_description']
                role = 'presenter'
            s.add(participation)
            logger.info('User [id {}] joined event [id {}] as [{}]'.format(user_id,
                                                                    event_id,
                                                                    role))
        else:
            raise JoinUserError('User has already joined this event as [{}]!'.format(is_consists.participation_role))
