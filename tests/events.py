from .requester import test_route
from colorama import init, Fore, Back, Style
import requests
import json


def test_events(cookies=None, cookies_not_admin=None):
    descriptions = [
    'CREATE EVENT wrong keys',
    'CREATE EVENT wrong date/time',
    'CREATE EVENT correct',
    'GET EVENT wrong id',
    'GET EVENT correct',
    'GET EVENT correct with creator cookie',
    'CREATE EVENT correct via non-admin',
    'UPDATE EVENT not owned',
    'UPDATE EVENT admin',
    'GET EVENT updated',
    'UPDATE EVENT wrong keys',
    'UPDATE EVENT owner',
    'ALL EVENTs no query',
    'ALL EVENTs wrong query',
    'ALL EVENTs correct query',
    'JOIN admin 2 viewer',
    'JOIN wrong id',
    'JOIN repeat join',
    'JOIN user 1 presenter',
    'GET PRESENTERS 1',
    'GET PRESENTERS 2',
    ]

    codes = [
    '<Response [400]>',
    '<Response [422]>',
    '<Response [201]>',
    '<Response [404]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [201]>',
    '<Response [403]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [400]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [404]>',
    '<Response [409]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [200]>',
    ]

    datas = [
    {'error': 'Wrong json key(s)!'},
    {'error': 'Incorrect date or time format'},
    {'extra': '1'},
    {'error': 'No event with this id'},
    {},
    {},
    {'extra': '2'},
    {'error': 'No rights!'},
    {'description': 'Successfully updated.'},
    {},
    {'error': 'Wrong json key(s)!'},
    {'description': 'Successfully updated.'},
    [],
    [],
    [],
    {'description': 'Successfully joined'},
    {'error': 'No event with this id'},
    {'error': 'User has already joined this event as [viewer]!'},
    {'description': 'Successfully joined'},
    [],
    [],
    ]

    i = 0
    code_passed = 0
    data_passed = 0
    data_skipped = 0

    if cookies is None:
        data = {
            "email": "root_mail",
            "password": "1234"
        }
        answer = requests.post('http://127.0.0.1:45000/login', data=json.dumps(data), headers={'Content-type': 'application/json'})
        cookies = answer.cookies
    if cookies_not_admin is None:
        data = {
            "email": "mail@mail",
            "name": "Name",
            "surname": "Surname",
            "password": "1234"
        }
        answer = requests.post('http://127.0.0.1:45000/register', data=json.dumps(data), headers={'Content-type': 'application/json'})
        data = {
            "email": "mail@mail",
            "password": "1234"
        }
        answer = requests.post('http://127.0.0.1:45000/login', data=json.dumps(data), headers={'Content-type': 'application/json'})
        cookies_not_admin = answer.cookies

    print(Fore.BLACK + Back.WHITE + '==========================( TESTS EVENTS )=========================' + Style.RESET_ALL)
    print()

    # create event wrong keys
    data = {
        "name": "naaaaame",
        "sm_descriprion": "sm_descriprion",
        "name": "kek"
    }
    i, code_passed, data_passed, data_skipped = test_route('/event/', cookies, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # create event wornd date/time data
    data = {
        "name": "naaaaame",
        "sm_descriprion": "sm_descriprion",
        "description": "description",
        "start_date": "10",
        "start_time": "",
        "location": "location",
        "site_link": "site_link",
        "additional_info": "additional_info"
    }
    i, code_passed, data_passed, data_skipped = test_route('/event/', cookies, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # create event correct
    data = {
        "name": "naaaaame",
        "sm_description": "sm_descriprion",
        "description": "description",
        "start_date": "2020-02-27",
        "start_time": "23:59",
        "location": "location",
        "site_link": "site_link",
        "additional_info": "additional_info"
    }
    i, code_passed, data_passed, data_skipped = test_route('/event/', cookies, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get event info wrong id
    i, code_passed, data_passed, data_skipped = test_route('/event/10', '', 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get event info correct
    i, code_passed, data_passed, data_skipped = test_route('/event/1', '', 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    data = {}
    # get event info correct
    i, code_passed, data_passed, data_skipped = test_route('/event/1', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    # create event correct via on-admin
    data = {
        "name": "11",
        "sm_description": "22",
        "description": "33",
        "start_date": "2222-02-27",
        "start_time": "23:59",
        "location": "44",
        "site_link": "55",
        "additional_info": "66"
    }
    i, code_passed, data_passed, data_skipped = test_route('/event/', cookies_not_admin, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # update event not own event
    data = {
        "name": "11",
        "sm_description": "22",
        "description": "33",
        "start_date": "2222-02-27",
    }
    i, code_passed, data_passed, data_skipped = test_route('/event/1', cookies_not_admin, 'put', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # update event admin
    data = {
        "name": "change",
        "start_date": "3333-02-27",
    }
    i, code_passed, data_passed, data_skipped = test_route('/event/2', cookies, 'put', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get event updated
    i, code_passed, data_passed, data_skipped = test_route('/event/2', '', 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    # update event wrong keys
    data = {
        "na": "changed name",
        "start_date": "3333-02-27",
    }
    i, code_passed, data_passed, data_skipped = test_route('/event/2', cookies, 'put', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # update event wrong keys
    data = {
        "name": "kekekekeke",    }
    i, code_passed, data_passed, data_skipped = test_route('/event/2', cookies_not_admin, 'put', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get event all
    i, code_passed, data_passed, data_skipped = test_route('/event/all', '', 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    data = {}
    # get event all
    i, code_passed, data_passed, data_skipped = test_route('/event/all?offset=5&size=10', '', 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get event all
    i, code_passed, data_passed, data_skipped = test_route('/event/all?offset=1&size=1', '', 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    # admin join event 2 as viewer
    data = {
        "role": "viewer",
        "report": "report",
        "presenter_description": "presenter_description",
    }
    i, code_passed, data_passed, data_skipped = test_route('/event/2/join', cookies, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # join event wrong id
    data = {
        "role": "viewer",
        "report": "report",
        "presenter_description": "presenter_description",
    }
    i, code_passed, data_passed, data_skipped = test_route('/event/10/join', cookies, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # join repeat
    data = {
        "role": "viewer",
        "report": "report",
        "presenter_description": "presenter_description",
    }
    i, code_passed, data_passed, data_skipped = test_route('/event/2/join', cookies, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # user join event 1 as presenter
    data = {
        "role": "presenter",
        "report": "report",
        "presenter_description": "presenter_description",
    }
    i, code_passed, data_passed, data_skipped = test_route('/event/1/join', cookies_not_admin, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get presenters 1
    i, code_passed, data_passed, data_skipped = test_route('/event/1/presenters', '', 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    data = {}
    # get presenters 2
    i, code_passed, data_passed, data_skipped = test_route('/event/2/presenters', '', 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)


    print(Fore.BLACK + Back.WHITE + '=====================( TESTS EVENTS FINISHED )=====================' + Style.RESET_ALL)
    print('TESTS: ' + str(i))
    print('CODE:' + "      " + Back.GREEN + 'passed: ' + str(code_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - code_passed) + Style.RESET_ALL)
    print('DATA:' + "      " + Back.GREEN + 'passed: ' + str(data_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - data_passed - data_skipped) + Style.RESET_ALL+ "      " + Back.MAGENTA + 'skipped: ' + str(data_skipped) + Style.RESET_ALL)
    print()

    return i, code_passed, data_passed, data_skipped, cookies, cookies_not_admin
