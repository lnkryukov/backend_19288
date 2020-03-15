from .requester import test_route
from colorama import init, Fore, Back, Style
import requests
import json
import os
from .config import cfg


def test_tasks(cookies={}):
    tests = [
    {'description': 'CREATE EVENT test',
                    'url': '/event/',
                    'method': 'post',
                    'data': {"name": "test", "sm_description": "test",
                             "description": "test", "start_date": "2020-01-01",
                             "start_time": "00:01", "end_date": "2021-01-01", "location": "test",
                             "site_link": "test", "additional_info": "test"},
                    'valid_code': '<Response [201]>',
                    'valid_data': {'description': '4'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'ADD MANAGER test',
                    'url': '/event/4/manager',
                    'method': 'post',
                    'data': {"email": "mail@mail"},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'Successfully added manager'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'ADD MANAGER repeatedly',
                    'url': '/event/4/manager',
                    'method': 'post',
                    'data': {"email": "mail@mail"},
                    'valid_code': '<Response [409]>',
                    'valid_data': {'error': 'User has already joined this event as [manager]'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'ADD MANAGER joined admin',
                    'url': '/event/4/manager',
                    'method': 'post',
                    'data': {"email": cfg.SUPER_ADMIN_MAIL},
                    'valid_code': '<Response [409]>',
                    'valid_data': {'error': 'User has already joined this event as [creator]'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'ADD MANAGER wrong event',
                    'url': '/event/10/manager',
                    'method': 'post',
                    'data': {"email": cfg.SUPER_ADMIN_MAIL},
                    'valid_code': '<Response [404]>',
                    'valid_data': {'error': 'No event with this id'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'ADD MANAGER wrong email',
                    'url': '/event/4/manager',
                    'method': 'post',
                    'data': {"email": "kek"},
                    'valid_code': '<Response [404]>',
                    'valid_data': {'error': 'No user with this id'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'ADD MANAGER no rights',
                    'url': '/event/4/manager',
                    'method': 'post',
                    'data': {"email": "kek"},
                    'valid_code': '<Response [403]>',
                    'valid_data': {'error': 'No rights'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'CREATE TASK 1',
                    'url': '/event/4/task',
                    'method': 'post',
                    'data': {"name": "task1", "description": "task1", "deadline": "2021-01-01"},
                    'valid_code': '<Response [201]>',
                    'valid_data': {'description': 'Task was added'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'CREATE TASK 2',
                    'url': '/event/4/task',
                    'method': 'post',
                    'data': {"name": "task2", "description": "task2", "deadline": "2021-01-01"},
                    'valid_code': '<Response [201]>',
                    'valid_data': {'description': 'Task was added'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'CREATE TASK not creator',
                    'url': '/event/4/task',
                    'method': 'post',
                    'data': {"name": "task2", "description": "task2", "deadline": "2021-01-01"},
                    'valid_code': '<Response [403]>',
                    'valid_data': {'error': 'No rights'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'CREATE TASK no event',
                    'url': '/event/10/task',
                    'method': 'post',
                    'data': {"name": "task2", "description": "task2", "deadline": "2021-01-01"},
                    'valid_code': '<Response [404]>',
                    'valid_data': {'error': 'No event with this id'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'CREATE TASK wrong keys',
                    'url': '/event/4/task',
                    'method': 'post',
                    'data': {"kek": "task2", "description": "task2", "deadline": "2021-01-01"},
                    'valid_code': '<Response [400]>',
                    'valid_data': {'error': 'Wrong json key(s)'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'DELETE TASK wrong task',
                    'url': '/event/4/task/10000/delete',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [404]>',
                    'valid_data': {'error': 'No task with this id'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'DELETE TASK 1',
                    'url': '/event/4/task/1/delete',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'Task was deleted'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'DELETE TASK 2',
                    'url': '/event/4/task/2/delete',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [403]>',
                    'valid_data': {'error': 'No rights'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'DELETE TASK 1 repeat',
                    'url': '/event/4/task/1/delete',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [404]>',
                    'valid_data': {'error': 'No task with this id'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'MOVE TASK 2 to kek',
                    'url': '/event/4/task/2/move/kek',
                    'method': 'put',
                    'data': {},
                    'valid_code': '<Response [422]>',
                    'valid_data': {'error': 'Wrong status'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'MOVE TASK 2 not manager',
                    'url': '/event/4/task/2/move/kek',
                    'method': 'put',
                    'data': {},
                    'valid_code': '<Response [403]>',
                    'valid_data': {'error': 'No rights'},
                    'need_decision': False,
                    'cookie': 'admin',
                    'get_cookie': False
    },
    {'description': 'MOVE TASK 2 done',
                    'url': '/event/4/task/2/move/done',
                    'method': 'put',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': "Task's status was changed"},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'MOVE TASK 2 done repeat',
                    'url': '/event/4/task/2/move/done',
                    'method': 'put',
                    'data': {},
                    'valid_code': '<Response [409]>',
                    'valid_data': {'error': 'Task already have this status'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'GET TASKS',
                    'url': '/event/4/task/all',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [{'deadline': '2021-01-01', 'description': 'task2', 'id': 2, 'name': 'task2', 'status': 'done'}],
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'UPDATE TASK 2',
                    'url': '/event/4/task/2',
                    'method': 'put',
                    'data': {'name': 'update'},
                    'valid_code': '<Response [200]>',
                    'valid_data': {'description': 'Task was updated'},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'GET TASKS',
                    'url': '/event/4/task/all',
                    'method': 'get',
                    'data': {},
                    'valid_code': '<Response [200]>',
                    'valid_data': [{'deadline': '2021-01-01', 'description': 'task2', 'id': 2, 'name': 'update', 'status': 'done'}],
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    {'description': 'UPDATE TASK 2 wrong fields',
                    'url': '/event/4/task/2',
                    'method': 'put',
                    'data': {'status': 'update'},
                    'valid_code': '<Response [400]>',
                    'valid_data': {'error': "Can't change this field(s)"},
                    'need_decision': False,
                    'cookie': 'user',
                    'get_cookie': False
    },
    ]

    i = 0
    code_passed = 0
    data_passed = 0

    root_url = 'http://' + cfg.HOST + ':' + cfg.PORT

    if not hasattr(cookies, 'admin'):
        data = {
            "email": cfg.SUPER_ADMIN_MAIL,
            "password": "1234"
        }
        answer = requests.post(root_url + '/login', data=json.dumps(data), headers={'Content-type': 'application/json'})
        cookies['admin'] = answer.cookies
    if not hasattr(cookies, 'user'):
        data = {
            "email": "mail@mail",
            "name": "Name",
            "surname": "Surname",
            "password": "1234"
        }
        answer = requests.post(root_url + '/register', data=json.dumps(data), headers={'Content-type': 'application/json'})
        data = {
            "email": "mail@mail",
            "password": "1234"
        }
        answer = requests.post(root_url + '/login', data=json.dumps(data), headers={'Content-type': 'application/json'})
        cookies['user'] = answer.cookies
    if not hasattr(cookies, 'none'):
        cookies['none'] = ''


    print(Fore.BLACK + Back.WHITE + '==========================( TESTS USERS )==========================' + Style.RESET_ALL)
    print()


    for test in tests:
        if test['get_cookie']:
            i, code_passed, data_passed, cookies[test['to_cookie']] = test_route(i, code_passed, data_passed,
                                                                    test['description'],
                                                                    test['url'],
                                                                    test['method'],
                                                                    test['data'],
                                                                    test['valid_code'],
                                                                    test['valid_data'],
                                                                    test['need_decision'],
                                                                    cookies[test['cookie']],
                                                                    test['get_cookie']
            )
        else:
            i, code_passed, data_passed = test_route(i, code_passed, data_passed,
                                                                    test['description'],
                                                                    test['url'],
                                                                    test['method'],
                                                                    test['data'],
                                                                    test['valid_code'],
                                                                    test['valid_data'],
                                                                    test['need_decision'],
                                                                    cookies[test['cookie']],
                                                                    test['get_cookie']
            )

    print(Fore.BLACK + Back.WHITE + '======================( TESTS TASKS FINISHED )=====================' + Style.RESET_ALL)
    print('TESTS: ' + str(i))
    print('CODE:' + "      " + Back.GREEN + 'passed: ' + str(code_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - code_passed) + Style.RESET_ALL)
    print('DATA:' + "      " + Back.GREEN + 'passed: ' + str(data_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(i - data_passed) + Style.RESET_ALL)
    print()

    return i, code_passed, data_passed, cookies