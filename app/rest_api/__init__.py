from flask import jsonify, request, abort
import logging
from ..util import send_500_email


# answers

def make_ok(code, description):
    return jsonify(description=description), code


def make_4xx(code, description):
    logging.warning(str(code) + ' - [{}]'.format(description))
    return jsonify(error=description), code


def get_json():
    data = request.get_json()
    if data is None:
        make_4xx(415, 'Expected json')
    return data


# legacy

#def make_200(description=None, extra=None):
    #body = {}
    #if description:
        #body['description'] = description
    #if extra:
        #body['extra'] = extra
    #return jsonify(body)


#def make_201(extra=None):
    #body = {}
    #if extra:
        #body['extra'] = extra
    #return jsonify(body), 201


def make_400(err):
    error = 'Incorrect request!'
    if isinstance(err, KeyError) or isinstance(err, AttributeError):
        err = 'Wrong json key(s)'
    logging.warning('400 - [{}] '.format(str(err)))
    return jsonify(error=str(err)), 400


#def make_403(err='No access'):
    #logging.warning('403 - [{}]'.format(err))
    #return jsonify(error=err), 403


#def make_404(err):
    #logging.warning('404 - [{}]'.format(str(err)))
    #return jsonify(error=str(err)), 404


#def make_409(err):
    #logging.warning('409 - [{}]'.format(str(err)))
    #return jsonify(error=str(err)), 409


#def make_415(err='Wrong data'):
    #logging.warning('415 - [{}]'.format(str(err)))
    #return jsonify(error=str(err)), 415


def make_422(err):
    if isinstance(err, ValueError):
        err = 'Wrong data'
    if isinstance(err, IndexError):
        err = 'Incorrect date or time format'
    logging.warning('422 - [{}]'.format(str(err)))
    return jsonify(error=str(err)), 422


# errors handlers

def unauthorized(e):
    logging.warning('401 - [{}]'.format(e))
    return jsonify(error="Unauthorized"), 401


#def no_access(e):
    #logging.warning('403 - [{}]'.format(e))
    #return jsonify(error="No access"), 403


def not_found(e):
    logging.warning('404 - [{}]'.format(e.description))
    if e.description[0] == 'T':
        return jsonify(error="Unknown route"), 404
    return jsonify(error=e.description), 404


def method_not_allowed(e):
    logging.warning('405 - [{}]'.format(e))
    return jsonify(error="Wrong route method"), 405


#def wrong_request_type(e):
    #logging.warning('415 - [{}]'.format(e))
    #return jsonify(error="Wrong request type!"), 415


def server_500_error(e):
    logging.warning('500 - [{}]'.format(e))
    send_500_email(e)
    return jsonify(error="Server error, we're sorry"), 500
