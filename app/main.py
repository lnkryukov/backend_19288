from argparse import ArgumentParser
import logging
import urllib3
import bcrypt

import evapp
from evapp import db


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = ArgumentParser(description='Backend service of Events project')

    parser.add_argument('--create-tables', type=str, dest='password',
                        help='Creates data base tables before launch.')

    args = parser.parse_args()
    
    if args.password:
        pw = bcrypt.hashpw(str(args.password).encode('utf-8'), bcrypt.gensalt())
        db.create_tables(pw.decode('utf-8'))

    logging.info('Starting restful api backend server')
    evapp.run()


if __name__ == '__main__':
    main()
