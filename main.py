from argparse import ArgumentParser
import logging
import urllib3
import bcrypt
import logging
import logging.config

import app
from app import db
from app.config import cfg

def main():

    '''
    Логгирование нужно конфигурировать в самом начале какой-нибудь логгер может успеть 
    создаться раньше с дефольтным конфигом
    '''
    logging.config.dictConfig(cfg.LOGGING)

    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = ArgumentParser(description='Backend service of Events project')

    parser.add_argument('--create-tables', type=str, dest='password',
                        help='Creates data base tables before launch.')

    args = parser.parse_args()
    
    if args.password:
        pw = bcrypt.hashpw(str(args.password).encode('utf-8'), bcrypt.gensalt())
        db.create_tables(pw.decode('utf-8'))

    logging.info('Starting restful api backend server')
    app.run()


if __name__ == '__main__':
    main()
