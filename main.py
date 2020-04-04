from argparse import ArgumentParser
import logging
import urllib3
import bcrypt

import app
from app import db
from app.config import cfg


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = ArgumentParser(description='Backend service of Events project')

    parser.add_argument('--create-tables', action='store_true',
                        dest='create_tables',
                        help='Creates data base tables before launch.')

    args = parser.parse_args()
    
    if args.create_tables:
        pw = bcrypt.hashpw(str(cfg.SUPER_ADMIN_PASSWORD).encode('utf-8'), bcrypt.gensalt())
        db.create_tables(pw.decode('utf-8'))

    logging.info('Starting restful api backend server')
    logging.info('IP: ' + cfg.HOST + '  PORT: ' + str(cfg.PORT))
    app.run()


if __name__ == '__main__':
    main()
