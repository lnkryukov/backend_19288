from .config import cfg
from .db import User, get_session

import bcrypt
import time


def user_loader(uc_id):
    with get_session() as s:
        return s.query(User).filter(
                User.cookie_id == uc_id,
                User.account_status == 'active'
        ).one_or_none()


def check_user(email):
    with get_session() as s:
        return s.query(User).filter(
                User.email == email,
                User.account_status == 'active'
        ).one_or_none()
