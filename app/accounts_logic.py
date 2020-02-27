from .config import cfg
from .db import *
from . import util
import logging
from .exceptions import (NotJsonError, ConfirmationLinkError,
                         RegisterUserError, WrongIdError)

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

import bcrypt

from datetime import datetime
import requests
import os
import nanoid
import uuid


def register_user(email, name, surname, password, service_status='user'):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == email
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
                raise RegisterUserError('User with this email was banned')
            else:
                raise RegisterUserError('Trying to register existing user')
        else:
            user = User(email=email, name=name,
                        surname=surname, password=password,
                        service_status=service_status,
                        confirmation_link=confirmation_link)
            s.add(user)
        if cfg.DEFAULT_USER_STATUS == 'unconfirmed':
            util.send_email(email, confirmation_link)
        logging.info('Registering new user [{}]'.format(email))


def confirm_user(confirmation_link):
    with get_session() as s:
        user = s.query(User).filter(
                User.confirmation_link == confirmation_link
        ).one_or_none()
        if user:
            if user.account_status == 'unconfirmed':
                user.account_status = 'active'
                logging.info('User [{}] is confirmed'.format(user.email))
            else:
                raise ConfirmationLinkError('User is currently confirmed by this link')
        else:
            raise WrongIdError('No user with this confirmation link')


def change_password(u_id, old_password, new_password):
    with get_session() as s:
        user = s.query(User).filter(
                User.id == u_id
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


def close_all_sessions(u_id, password):
    with get_session() as s:
        user = s.query(User).filter(
                User.id == u_id
        ).one_or_none()
        opw = str(password).encode('utf-8')
        pw = str(user.password).encode('utf-8')
        if bcrypt.checkpw(opw, pw):
            user.cookie_id = uuid.uuid4()
            return user
        else:
            return None


def self_delete(u_id, password):
    with get_session() as s:
        user = s.query(User).filter(
                User.id == u_id
        ).one_or_none()
        opw = str(password).encode('utf-8')
        pw = str(user.password).encode('utf-8')
        if bcrypt.checkpw(opw, pw):
            user.account_status = 'deleted'
            user.cookie_id = uuid.uuid4()
            user.phone = None
            user.organization = None
            user.position = None
            user.country = None
            user.bio = None
            return 'ok'
        else:
            return ''


def ban_user(u_id):
    with get_session() as s:
        user = s.query(User).filter(
                User.id == u_id
        ).one_or_none()

        if not user:
            raise WrongIdError('No user with this id')
        user.account_status = 'banned'
