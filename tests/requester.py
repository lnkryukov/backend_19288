import requests
import json
from sys import exit
from colorama import init, Fore, Back, Style


root_url = 'http://127.0.0.1:45000'
json_headers = {'Content-type': 'application/json'}


def test_route(url, cookies, method, data, i, description, valid_code, valid_data, code_passed, data_passed, data_skipped, get_cookie, skippable):
    print(Back.BLUE + '=======================( TEST [' + str(i+1) + '] )=======================' + Style.RESET_ALL)
    print()
    print('url: ' + url)
    print('method: ' + method)
    print('test: ' + description)
    print()
    if method == 'post':
        if cookies:
            answer = requests.post(root_url + url, data=json.dumps(data), headers=json_headers, cookies=cookies)
        else:
            answer = requests.post(root_url + url, data=json.dumps(data), headers=json_headers)
    elif method == 'get':
        if cookies:
            answer = requests.get(root_url + url, cookies=cookies)
        else:
            answer = requests.get(root_url + url)
    elif method == 'put':
        if cookies:
            answer = requests.put(root_url + url, data=json.dumps(data), headers=json_headers, cookies=cookies)
        else:
            answer = requests.put(root_url + url, data=json.dumps(data), headers=json_headers)
    else:
        print(Back.RED + 'AZAZAZAZA' + Style.RESET_ALL)
        print(Back.RED + 'YOU WROTE WRONG METHOD IN TEST' + Style.RESET_ALL)
        exit()

    print(Back.BLUE + 'CODE TEST' + Style.RESET_ALL)
    print('Expects:')
    print(valid_code)
    print('Got:')
    print(answer)
    if str(answer) == valid_code:
        print(Back.GREEN + '>>CODE PASS' + Style.RESET_ALL)
        code_passed += 1
    else:
        print(Back.RED + '>>CODE ERR' + Style.RESET_ALL)
    response = answer.json()
    print()
    print(Back.BLUE + 'DATA TEST' + Style.RESET_ALL)
    print('Expects:')
    print(valid_data)
    print('Got:')
    print(response)
    if response == valid_data:
        print(Back.GREEN + '>>DATA PASS' + Style.RESET_ALL)
        data_passed += 1
    else:
        if skippable:
            print(Back.MAGENTA + '>>DATA SKIP' + Style.RESET_ALL)
            data_skipped += 1
        else:
            print(Back.RED + '>>DATA ERR' + Style.RESET_ALL)
    i += 1
    print()
    if get_cookie:
        return i, answer.cookies, code_passed, data_passed, data_skipped
    return i, code_passed, data_passed, data_skipped
