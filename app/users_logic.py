from .config import cfg
from .db import *
from . import util
from .exceptions import NotJsonError, NoData, ConfirmationLinkError

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

from datetime import datetime
import requests
import logging
import os
import nanoid


def user_info(user_id):
    with get_session() as s:
        user = s.query(User).get(user_id)

        return {
            "mail": user.mail,
            "name": user.name,
            "surname": user.surname,
            "service_status": user.service_status,
            "phone": user.phone,
            "organization": user.organization,
            "position": user.position,
            "country": user.country,
            "bio": user.bio
        }


def get_users():
    result = {}
    with get_session() as s:
        users = s.query(User).all()
        for user in users:
            result[user.id] = {
                'id': user.id,
                'mail': user.mail,
                'name': user.name,
                'surname': user.surname,
                'service_status': user.service_status,
                'account_status': user.account_status
            }
    return result


def update_profile(id, args):
    with get_session() as s:
        user = s.query(User).filter(
                User.id == id,
                User.account_status == 'active',
        ).one_or_none()

        for arg in args.keys():
            getattr(user, arg)
        for arg in args.keys():
            setattr(user, arg, args[arg])


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
                'start_date': event.start_date,
                'end_date': event.end_date,
                'start_time': event.start_time
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
                'start_date': event.start_date,
                'end_date': event.end_date,
                'start_time': event.start_time
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
                'start_date': event.start_date,
                'end_date': event.end_date,
                'start_time': event.start_time
            }

    return result_creator, result_presenter, result_participant


# deprecated version

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
