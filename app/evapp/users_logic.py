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


def register_user(mail, name, surname, password, service_status='user'):
    with get_session() as s:
        user = s.query(User).filter(
                User.mail == mail,
                User.account_status == 'deleted',
        ).one_or_none()

        # checking unique link
        confirmation_link = ''
        while True:
            confirmation_link = nanoid.generate(size=50)
            exists = s.query(User).filter(
                    User.confirmation_link == confirmation_link
            ).one_or_none()
            if not exists:
                break

        if user:
            user.account_status = cfg.DEFAULT_USER_STATUS
            user.confirmation_link = confirmation_link
            user.service_status = service_status
        else:
            user = User(mail=mail, name=name,
                        surname=surname, password=password,
                        service_status=service_status,
                        confirmation_link=confirmation_link)
            s.add(user)
        if cfg.DEFAULT_USER_STATUS == 'unconfirmed':
            util.send_email(mail, confirmation_link)
        logging.info('Registering new user [{}]'.format(mail))


def confirm_user(confirmation_link):
    with get_session() as s:
        user = s.query(User).filter(
                User.confirmation_link == confirmation_link,
                User.status == 'unconfirmed',
        ).one_or_none()
        if user:
            user.status = 'active'
            logging.info('User [{}] is confirmed'.format(user.mail))
            return 'user confirmed'
        else:
            return 'user is currently confirmed by this link'


def get_users():
    result = {}
    with get_session() as s:
        users = s.query(User).all()
        for user in users:
            result[user.id] = {
                'mail': user.mail,
                'name': user.name,
                'surname': user.surname,
            }
    return result


def update_profile(id, args):
    with get_session() as s:
        user = s.query(User).filter(
                User.id == id,
                User.status == 'active',
        ).one_or_none()

        if 'name' in args.keys():
            user.name = args['name']
        if 'surname' in args.keys():
            user.surname = args['surname']
        if 'phone' in args.keys():
            user.phone = args['phone']
        if 'organization' in args.keys():
            user.organization = args['organization']
        if 'position' in args.keys():
            user.position = args['position']
        if 'country' in args.keys():
            user.country = args['country']


def get_user_stat(user_id):
    result_creator = {}
    result_presenter = {}
    result_participant = {}
    with get_session() as s:
        as_creator = s.query(Participation, Event).filter(
                Participation.event == Event.id,
                Participation.participant == user_id,
                Participation.participation_role == 'creator'
        ).all()

        for participant, event in as_creator:
            result_creator[event.id] = {
                'id': event.id,
                'name': event.name,
                'date': event.date_time,
            }

        as_presenter = s.query(Participation, Event).filter(
                Participation.event == Event.id,
                Participation.participant == user_id,
                Participation.participation_role == 'presenter'
        ).all()

        for participant, event in as_presenter:
            result_presenter[event.id] = {
                'id': event.id,
                'name': event.name,
                'date': event.date_time,
            }

        as_participant = s.query(Participation, Event).filter(
                Participation.event == Event.id,
                Participation.participant == user_id,
                Participation.participation_role == 'participant'
        ).all()

        for participant, event in as_participant:
            result_participant[event.id] = {
                'id': event.id,
                'name': event.name,
                'date': event.date_time,
            }

    return result_creator, result_presenter, result_participant
