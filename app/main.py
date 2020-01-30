from argparse import ArgumentParser
import logging
from main import db, rest_cookie, rest_token
import urllib3
import bcrypt


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = ArgumentParser(description='Backend service of Events project')

    parser.add_argument('role', metavar='role', type=str,
                        help='A type of rest auth variant: with cookies (rest_cookie) or tokens (rest_token)')
    parser.add_argument('--create-tables', type=str, dest='password',
                        help='Creates data base tables before launch.')

    args = parser.parse_args()
    
    if args.password:
        db.create_tables(bcrypt.hashpw(args.password, bcrypt.gensalt()))

    if args.role == 'rest_cookie':
        logging.info('Starting restful api backend server with cookies auth')
        rest_cookie.run()
    elif args.role == 'rest_token':
        logging.info('Starting restful api backend server with token auth')
        rest_token.run()
    else:
        logging.critical('Unknown role, exit...')


if __name__ == '__main__':
    main()
