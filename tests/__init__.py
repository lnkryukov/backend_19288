from colorama import init, Fore, Back, Style
from .accounts import test_accounts
from .users import test_users
from .events import test_events


init()

print(Fore.BLACK + Back.WHITE + '=========================( TESTS STARTED )=========================' + Style.RESET_ALL)
print()
print(Fore.BLACK + Back.WHITE + '==========================( RESETING DB )==========================' + Style.RESET_ALL)
print()


def run():
    print()
    global_i = 0
    global_code_passed = 0
    global_data_passed = 0
    global_data_skipped = 0

    cookies = None
    cookies_not_admin = None

    i, code_passed, data_passed, data_skipped, cookies, cookies_not_admin = test_accounts()
    global_i += i
    global_code_passed += code_passed
    global_data_passed += data_passed
    global_data_skipped += data_skipped

    i, code_passed, data_passed, data_skipped, cookies, cookies_not_admin = test_events(cookies, cookies_not_admin)
    global_i += i
    global_code_passed += code_passed
    global_data_passed += data_passed
    global_data_skipped += data_skipped

    i, code_passed, data_passed, data_skipped = test_users(cookies, cookies_not_admin)
    global_i += i
    global_code_passed += code_passed
    global_data_passed += data_passed
    global_data_skipped += data_skipped

    print(Fore.BLACK + Back.WHITE + '========================( ALL TESTS OVER )=========================' + Style.RESET_ALL)
    print('TESTS: ' + str(global_i))
    print('CODE:' + "      " + Back.GREEN + 'passed: ' + str(global_code_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(global_i - global_code_passed) + Style.RESET_ALL)
    print('DATA:' + "      " + Back.GREEN + 'passed: ' + str(global_data_passed) + Style.RESET_ALL + "      " + Back.RED + 'failed: ' + str(global_i - global_data_passed - global_data_skipped) + Style.RESET_ALL+ "      " + Back.MAGENTA + 'skipped: ' + str(global_data_skipped) + Style.RESET_ALL)
