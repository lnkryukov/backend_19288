from .config import cfg
from .db import *
from . import util
from . import logger
from .exceptions import (NotJsonError, NoData, ConfirmationLinkError,
                         RegisterUserError, WrongIdError)

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

import bcrypt

from datetime import datetime
import requests
import os
import nanoid
import uuid


def register_user(mail, name, surname, password, service_status='user'):
    with get_session() as s:
        user = s.query(User).filter(
                User.mail == mail
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
            if user.account_status == 'deleted':
                user.password = password
                user.name = name
                user.surname = surname
                user.account_status = cfg.DEFAULT_USER_STATUS
                user.confirmation_link = confirmation_link
                user.service_status = service_status
            elif user.account_status == 'banned':
                raise RegisterUserError('User with this mail was banned')
            else:
                raise RegisterUserError('Trying to register existing user')
        else:
            user = User(mail=mail, name=name,
                        surname=surname, password=password,
                        service_status=service_status,
                        confirmation_link=confirmation_link)
            s.add(user)
        if cfg.DEFAULT_USER_STATUS == 'unconfirmed':
            util.send_email(mail, confirmation_link)
        logger.info('Registering new user [{}]'.format(mail))


def confirm_user(confirmation_link):
    with get_session() as s:
        user = s.query(User).filter(
                User.confirmation_link == confirmation_link
        ).one_or_none()
        if user:
            if user.account_status == 'unconfirmed':
                user.account_status = 'active'
                logger.info('User [{}] is confirmed'.format(user.mail))
            else:
                raise ConfirmationLinkError('User is currently confirmed by this link')
        else:
            raise WrongIdError('No user with this confirmation link')


def change_password(user_id, old_password, new_password):
    with get_session() as s:
        user = s.query(User).filter(
                User.id == user_id
        ).one_or_none()
        opw = str(old_password).encode('utf-8')
        pw = str(user.password).encode('utf-8')
        if bcrypt.checkpw(opw, pw):
            npw = bcrypt.hashpw(str(new_password).encode('utf-8'),
                               bcrypt.gensalt())
            user.password = npw.decode('utf-8')
            user.cookie_id = uuid.uuid4()
            return user
        else:
            return None


def close_all_sessions(user_id, old_password):
    with get_session() as s:
        user = s.query(User).filter(
                User.id == user_id
        ).one_or_none()
        opw = str(old_password).encode('utf-8')
        pw = str(user.password).encode('utf-8')
        if bcrypt.checkpw(opw, pw):
            user.cookie_id = uuid.uuid4()
            return user
        else:
            return None


def self_delete(user_id):
    with get_session() as s:
        user = s.query(User).filter(
                User.id == user_id
        ).one_or_none()

        user.account_status = 'deleted'
        user.phone = None
        user.organization = None
        user.position = None
        user.country = None
        user.bio = None


def ban_user(user_id):
    with get_session() as s:
        user = s.query(User).filter(
                User.id == user_id
        ).one_or_none()

        if not user:
            raise WrongIdError('No user with this id')
        user.account_status = 'banned'
