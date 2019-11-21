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
            confirmation_link = random_string_digits(25)
            user = User(login=login, mail=mail, name=name,
                        surname=surname, password=password,
                        lvl=lvl, confirmation_link=confirmation_link)
            s.add(user)
        logging.info('Registering new user [{}]'.format(login))


def confirm_user(confirmation_link):
    with get_session() as s:
        user = s.query(User).filter(
                User.confirmation_link == confirmation_link,
                User.status == 'unconfirmed',
        ).one_or_none()
        if user:
            user.status = 'active'
