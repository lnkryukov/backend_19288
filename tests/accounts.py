from .requester import test_route
from colorama import init, Fore, Back, Style


def test_accounts():
    descriptions = [
    'LOGIN with incorrect email',
    'LOGIN with incorrect password',
    'LOGIN with incorrect keys',
    'LOGIN correct',
    'LOGIN repeat correct',
    'LOGOUT correct',
    'REGISTER correct',
    'REGISTER user exists',
    'REGISTER then login',
    'LOGIN mail@mail.mail',
    'CHANGE PASSWORD incorrect old password',
    'CHANGE PASSWORD correct',
    'CHANGE PASSWORD old cookie try',
    'CHANGE PASSWORD correct with new cookies',
    'CLOSE ALL SESSIONS correct',
    'SELF DELETE correct',
    'LOGIN REQUIRED ROUTE AFTER SELF DELETE',
    'LOGIN AFTER SELF DELETE',
    'REGISTER AFTER SELF DELETE',
    'LOGIN AFTER SELF DELETE AND REREGISTERING',
    'USER BAN USER',
    'ADMIN BAN 404 USER',
    'ADMIN BAN USER',
    'LOGIN BANNED USER',
    'REGISTER BANNED USER',
    'REGISTER new user correct',
    'LOGIN new user correct'
    ]

    codes = [
    '<Response [404]>',
    '<Response [422]>',
    '<Response [400]>',
    '<Response [200]>',
    '<Response [409]>',
    '<Response [200]>',
    '<Response [201]>',
    '<Response [409]>',
    '<Response [409]>',
    '<Response [200]>',
    '<Response [422]>',
    '<Response [200]>',
    '<Response [401]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [200]>',
    '<Response [401]>',
    '<Response [404]>', # move to 409 deleted
    '<Response [201]>',
    '<Response [200]>',
    '<Response [403]>',
    '<Response [404]>',
    '<Response [200]>',
    '<Response [404]>', # move to 409 banned
    '<Response [409]>',
    '<Response [201]>',
    '<Response [200]>'
    ]

    datas = [
    {'error': 'Invalid user'},
    {'error': 'Invalid password'},
    {'error': 'Wrong json key(s)!'},
    {'description': 'User was logined', 'extra': 'admin'},
    {'error': 'User is currently authenticated!'},
    {'description': 'User was logouted'},
    {'extra': 'User was registered.'},
    {'error': 'Trying to register existing user'},
    {'error': 'User is currently authenticated!'},
    {'description': 'User was logined', 'extra': 'user'},
    {'error': 'Invalid password'},
    {'description': 'Password has beed changed', 'extra': 'user'},
    {'error': 'Unauthorized'},
    {'description': 'Password has beed changed', 'extra': 'user'},
    {'description': 'Logout from all other sessions.', 'extra': 'user'},
    {'description': 'Successfully delete account.'},
    {'error': 'Unauthorized'},
    {'error': 'Invalid user'},
    {'extra': 'User was registered.'},
    {'description': 'User was logined', 'extra': 'user'},
    {'error': 'No rights!'},
    {'error': 'No user with this id'},
    {'description': 'Successfully baned this user'},
    {'error': 'Invalid user'},
    {'error': 'User with this email was banned'},
    {'extra': 'User was registered.'},
    {'description': 'User was logined', 'extra': 'user'}
    ]

    cookies = ''
    cookies_not_admin = ''
    i = 0
    code_passed = 0
    data_passed = 0
    data_skipped = 0

    print(Fore.BLACK + Back.WHITE + '=========================( TESTS ACCOUNT )=========================' + Style.RESET_ALL)
    print()

    # login
    # incorrect email
    data = {
        "email": "root",
        "password": "1234"
    }
    i, code_passed, data_passed, data_skipped = test_route('/login', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # incorrect password
    data = {
        "email": "root_mail",
        "password": "123456789"
    }
    i, code_passed, data_passed, data_skipped = test_route('/login', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # incorrect keys
    data = {
        "mail": "root_mail",
        "password": "1234"
    }
    i, code_passed, data_passed, data_skipped = test_route('/login', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # correct login
    data = {
        "email": "root_mail",
        "password": "1234"
    }
    i, cookies, code_passed, data_passed, data_skipped = test_route('/login', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, True, False)

    # repeat correct login
    data = {
        "email": "root_mail",
        "password": "1234"
    }
    i, code_passed, data_passed, data_skipped = test_route('/login', cookies, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # logout
    i, code_passed, data_passed, data_skipped = test_route('/logout', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # register correct
    data = {
        "email": "mail@mail.mail",
        "name": "naaaaaaaame",
        "surname": "surnaaaaaaaame",
        "password": "1234"
    }
    i, code_passed, data_passed, data_skipped = test_route('/register', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # register user exists
    data = {
        "email": "root_mail",
        "name": "naaaaaaaame",
        "surname": "surnaaaaaaaame",
        "password": "1234"
    }
    i, code_passed, data_passed, data_skipped = test_route('/register', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # register user exists
    data = {
        "email": "root_mail",
        "password": "1234"
    }
    i, code_passed, data_passed, data_skipped = test_route('/register', cookies, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # correct login mail@mail.mail
    data = {
        "email": "mail@mail.mail",
        "password": "1234"
    }
    i, cookies_not_admin, code_passed, data_passed, data_skipped = test_route('/login', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, True, False)

    # change password wrong old
    data = {
        "old_password": "12345",
        "new_password": "12345678"
    }
    i, code_passed, data_passed, data_skipped = test_route('/change_password', cookies_not_admin, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)


    # change password correct
    data = {
        "old_password": "1234",
        "new_password": "12345678"
    }
    new_cookie = ''
    i, new_cookie, code_passed, data_passed, data_skipped = test_route('/change_password', cookies_not_admin, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, True, False)


    # change password with old cookie
    data = {
        "old_password": "12345678",
        "new_password": "1234567890"
    }
    i, code_passed, data_passed, data_skipped = test_route('/change_password', cookies_not_admin, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)


    # change password with new cookie
    data = {
        "old_password": "12345678",
        "new_password": "1234"
    }
    i, cookies_not_admin, code_passed, data_passed, data_skipped = test_route('/change_password', new_cookie, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, True, False)

    # close all sessions correct
    data = {
        "password": "1234"
    }
    i, cookies_not_admin, code_passed, data_passed, data_skipped = test_route('/close_all_sessions', cookies_not_admin, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, True, False)

    # self delete
    data = {
        "password": "1234"
    }
    i, code_passed, data_passed, data_skipped = test_route('/delete', cookies_not_admin, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # trying something after self deleting
    data = {
        "old_password": "12345678",
        "new_password": "1234567890"
    }
    i, code_passed, data_passed, data_skipped = test_route('/change_password', cookies_not_admin, 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # login mail@mail.mail then deleted
    data = {
        "email": "mail@mail.mail",
        "password": "1234"
    }
    i, code_passed, data_passed, data_skipped = test_route('/login', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # register after self deleting
    data = {
        "email": "mail@mail.mail",
        "name": "name",
        "surname": "surname",
        "password": "1234"
    }
    i, code_passed, data_passed, data_skipped = test_route('/register', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # correct login mail@mail.mail
    data = {
        "email": "mail@mail.mail",
        "password": "1234"
    }
    i, cookies_not_admin, code_passed, data_passed, data_skipped = test_route('/login', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, True, False)

    # user ban user
    i, code_passed, data_passed, data_skipped = test_route('/user/2/ban', cookies_not_admin, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # admin bans 404 user
    i, code_passed, data_passed, data_skipped = test_route('/user/10/ban', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # admin bans user
    i, code_passed, data_passed, data_skipped = test_route('/user/2/ban', cookies, 'get', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # banned login mail@mail.mail
    data = {
        "email": "mail@mail.mail",
        "password": "1234"
    }
    i, code_passed, data_passed, data_skipped = test_route('/login', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # register after self deleting
    data = {
        "email": "mail@mail.mail",
        "name": "name",
        "surname": "surname",
        "password": "1234"
    }
    i, code_passed, data_passed, data_skipped = test_route('/register', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # register new
    data = {
        "email": "mail@mail",
        "name": "Name",
        "surname": "Surname",
        "password": "1234"
    }
    i, code_passed, data_passed, data_skipped = test_route('/register', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, False, False)

    # login new mail@mail
    data = {
        "email": "mail@mail",
        "password": "1234"
    }
    i, cookies_not_admin, code_passed, data_passed, data_skipped = test_route('/login', '', 'post', data, i, descriptions[i], codes[i], datas[i], code_passed, data_passed, data_skipped, True, False)

    print(Fore.BLACK + Back.WHITE + '=====================( TESTS ACCOUNT FINISHED )====================' + Style.RESET_ALL)
    print('TESTS: ' + str(i))
    print('CODE:' + "      " + Back.GREEN + 'passed: ' + str(code_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - code_passed) + Style.RESET_ALL)
    print('DATA:' + "      " + Back.GREEN + 'passed: ' + str(data_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - data_passed - data_skipped) + Style.RESET_ALL+ "      " + Back.MAGENTA + 'skipped: ' + str(data_skipped) + Style.RESET_ALL)
    print()

    return i, code_passed, data_passed, data_skipped, cookies, cookies_not_admin
