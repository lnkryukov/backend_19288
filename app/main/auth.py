from . import cfg
from .db import User, get_session

from passlib.hash import sha256_crypt
import jwt
import time


def user_loader(user_id):
    with get_session() as s:
        return s.query(User).filter(
                User.cookie_id == user_id
        ).one_or_none()


def check_user(mail):
    with get_session() as s:
        return s.query(User).filter(
                User.mail == mail,
                User.status == 'active'
        ).one_or_none()


# tokens

def header_loader(header):
    try:
        token = jwt.decode(header, 'secret', algorithms=['HS256'])
    except jwt.exceptions.InvalidTokenError:
        return None
    with get_session() as s:
        pair = s.query(User, Token).filter(
                User.id == token['uid'],
                Token.id == token['jti'],
                Token.status == 'active',
        ).one_or_none()
        return pair[0] if pair else None


def get_jwt(token):
    payload = {
        'jti': str(token.id),
        'iat': token.issued,
        'uid': token.vmuser_id,
    }
    t = jwt.encode(payload, 'secret', 'HS256').decode('utf-8')
    return t


def get_token(user):
    with get_session() as s:
        token = s.query(Token).filter(
                Token.vmuser_id == user.id,
                Token.status == 'active'
        ).one_or_none()
        if not token:
            return None
        return get_jwt(token)


def issue_token(user):
    with get_session() as s:
        old_token = s.query(Token).filter(
                Token.vmuser_id == user.id,
                Token.status == 'active'
        ).one_or_none()
        if old_token:
            old_token.status = 'deleted'
        token = Token()
        token.vmuser_id = user.id
        s.add(token)
        s.flush()
        return get_jwt(token)
