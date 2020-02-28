from .requester import test_route
from colorama import init, Fore, Back, Style
import requests
import json

def test_users(cookies=None, cookies_not_admin=None):
    descriptions = [
    'GET CURRENT USER INFO',
    'GET CURRENT USER STATUS',
    'PUT CURRENT USER email or password failed',
    'PUT CURRENT USER correct',
    'GET CURRENT USER INFO updated',
    'GET CURRENT USER EVENTS with incorrect role',
    'GET CURRENT USER EVENTS admin creator',
    'GET CURRENT USER EVENTS admin manager',
    'GET CURRENT USER EVENTS admin paresenter',
    'GET CURRENT USER EVENTS admin viewer',
    'GET CURRENT USER EVENTS user creator',
    'GET CURRENT USER EVENTS user manager',
    'GET CURRENT USER EVENTS user paresenter',
    'GET CURRENT USER EVENTS user viewer',
    'GET ALL USERS non-admin',
    'GET ALL USERS admin',
    'GET USER INFO non-admin',
    'GET USER INFO admin',
    'GET USER INFO admin not found',
    'GET USER EVENTS presenter admin not found',
    'GET USER EVENTS presenter admin',
    'GET USER EVENTS presenter non-admin',
    ]

    codes = [
    '<Response [200]>',
    '<Response [200]>',
    '<Response [400]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [404]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [403]>',
    '<Response [200]>',
    '<Response [403]>',
    '<Response [200]>',
    '<Response [404]>',
    '<Response [404]>',
    '<Response [200]>',
    '<Response [403]>',
    ]

    datas = [
    {
    'bio': None, 'country': None, 'email': 'root_mail',
    'name': 'Name', 'organization': None, 'phone': None,
    'position': None, 'service_status': 'admin', 'surname': 'Surname'
    },
    {'service_status': 'admin'},
    {'error': 'No email or password changing here'},
    {'description': 'Profile info successfully updated.'},
    {
    'bio': None, 'country': None, 'email': 'root_mail',
    'name': 'kek', 'organization': None, 'phone': "88005553535",
    'position': None, 'service_status': 'admin', 'surname': 'Surname'
    },
    {'error': 'Unknown route!'},
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    {'error': 'No rights!'},
    [],
    {'error': 'AccessError - No rights.'},
    {},
    {'error': 'No user with this id'},
    {'error': 'No user with this id'},
    {},
    {'error': 'AccessError - No rights.'},
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

    print(Fore.BLACK + Back.WHITE + '==========================( TESTS USERS )==========================' + Style.RESET_ALL)
    print()

    data = {}
    # get user info
    i, code_passed, data_passed, data_skipped = test_route('/user/', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)


    # get user status
    i, code_passed, data_passed, data_skipped = test_route('/user/status', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # wrong put
    data = {
        "email": "mail@mail",
        "password": "1234",
        "name": "kek"
    }
    i, code_passed, data_passed, data_skipped = test_route('/user/', cookies, 'put', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # correct put
    data = {
        "name": "kek",
        "phone": "88005553535"
    }
    i, code_passed, data_passed, data_skipped = test_route('/user/', cookies, 'put', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # get updated user info
    i, code_passed, data_passed, data_skipped = test_route('/user/', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get user events by role
    i, code_passed, data_passed, data_skipped = test_route('/user/events/kek', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get admin events creator
    i, code_passed, data_passed, data_skipped = test_route('/user/events/creator', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    data = {}
    # get admin events manager
    i, code_passed, data_passed, data_skipped = test_route('/user/events/manager', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get admin events presenter
    i, code_passed, data_passed, data_skipped = test_route('/user/events/presenter', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get admin events viewer
    i, code_passed, data_passed, data_skipped = test_route('/user/events/viewer', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    data = {}
    # get user events creator
    i, code_passed, data_passed, data_skipped = test_route('/user/events/creator', cookies_not_admin, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    data = {}
    # get user events manager
    i, code_passed, data_passed, data_skipped = test_route('/user/events/manager', cookies_not_admin, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get user events presenter
    i, code_passed, data_passed, data_skipped = test_route('/user/events/presenter', cookies_not_admin, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    data = {}
    # get user events viewer
    i, code_passed, data_passed, data_skipped = test_route('/user/events/viewer', cookies_not_admin, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get all users non-admin
    i, code_passed, data_passed, data_skipped = test_route('/user/all', cookies_not_admin, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get all users admin
    i, code_passed, data_passed, data_skipped = test_route('/user/all', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    data = {}
    # get user via non-admin
    i, code_passed, data_passed, data_skipped = test_route('/user/1', cookies_not_admin, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get user via admin
    i, code_passed, data_passed, data_skipped = test_route('/user/2', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    data = {}
    # get user via admin
    i, code_passed, data_passed, data_skipped = test_route('/user/20', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    data = {}
    # get user events presenter via admin no user
    i, code_passed, data_passed, data_skipped = test_route('/user/10/events/presenter', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    data = {}
    # get user events presenter via admin
    i, code_passed, data_passed, data_skipped = test_route('/user/2/events/presenter', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, True)

    data = {}
    # get user events presenter via non-admin
    i, code_passed, data_passed, data_skipped = test_route('/user/2/events/presenter', cookies_not_admin, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)


    print(Fore.BLACK + Back.WHITE + '======================( TESTS USERS FINISHED )=====================' + Style.RESET_ALL)
    print('TESTS: ' + str(i))
    print('CODE:' + "      " + Back.GREEN + 'passed: ' + str(code_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - code_passed) + Style.RESET_ALL)
    print('DATA:' + "      " + Back.GREEN + 'passed: ' + str(data_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - data_passed - data_skipped) + Style.RESET_ALL+ "      " + Back.MAGENTA + 'skipped: ' + str(data_skipped) + Style.RESET_ALL)
    print()

    return i, code_passed, data_passed, data_skipped
