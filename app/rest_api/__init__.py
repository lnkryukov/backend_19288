from flask import jsonify, make_response
import logging


# answers

def make_200(description=None, extra=None):
    if description:
        body['description'] = description
    if extra:
        body['extra'] = extra
    return jsonify(body)


def make_201(extra=None):
    if extra:
        body['extra'] = extra
    return jsonify(body), 201


def make_400(err):
    error = 'Incorrect request!'
    if isinstance(err, KeyError) or isinstance(err, AttributeError):
        err = 'Wrong json key(s)!'
    logging.warning('400 - [{}] '.format(str(err)))
    return jsonify(error=str(err)), 400


def make_403(err='No access'):
    logging.warning('403 - [{}]'.format(err))
    return jsonify(error=err), 403


def make_404(err):
    logging.warning('404 - [{}]'.format(str(err)))
    return jsonify(error=str(err)), 404


def make_409(err):
    logging.warning('409 - [{}]'.format(str(err)))
    return jsonify(error=str(err)), 409


def make_415(err='Wrong data'):
    logging.warning('415 - [{}] [{}]'.format(err))
    return jsonify(error=err), 415


def make_422(err):
    if isinstance(err, ValueError):
        err = 'Offset or size has wrong data!'
    logging.warning('422 - [{}] '.format(str(err)))
    return jsonify(error=str(err)), 422


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
