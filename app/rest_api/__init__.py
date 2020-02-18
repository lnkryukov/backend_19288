from flask import jsonify, make_response
import logging


# answers

def make_200(description=None, extra=None):
    body = {
        'status': 'ok',
    }
    if description:
        body['description'] = description
    if extra:
        body['extra'] = extra
    return jsonify(body)


def make_201(extra=None):
    body = {
        'status': 'Created',
    }
    if extra:
        body['extra'] = extra
    return jsonify(body), 201


def make_400(text='Invalid reqeust'):
    logging.warning('400 - [{}]'.format(text))
    return jsonify(error=text), 400


def make_404(text='No resource'):
    logging.warning('404 - [{}]'.format(text))
    return jsonify(error=text), 404


def make_415(text='Wrong data', e=''):
    logging.exception('415 - [{}] [{}]'.format(text, e))
    return jsonify(error=text), 415


def make_422(text='Wrong data'):
    logging.exception('422 - [{}] '.format(text))
    return jsonify(error=text), 422


# errors handlers

def unauthorized(e):
    logging.warning('401 - [{}]'.format(e))
    return jsonify(error="Unauthorized"), 401


def no_access(e):
    logging.warning('403 - [{}]'.format(e))
    return jsonify(error="No access"), 403


def route_not_found(e):
    logging.warning('404 - [{}]'.format(e))
    return jsonify(error="Unknown route!"), 404


def method_not_allowed(e):
    logging.warning('405 - [{}]'.format(e))
    return jsonify(error="Wrong route method!"), 405


def wrong_request_type(e):
    logging.warning('415 - [{}]'.format(e))
    return jsonify(error="Wrong request type!"), 415
