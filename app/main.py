from argparse import ArgumentParser
import logging
from evproj import db, server
import urllib3
from passlib.hash import sha256_crypt


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = ArgumentParser(description='Backend service of Events project')
    parser.add_argument('--create-tables', type=str, dest='password',
                        help='Creates data base tables before launch.')
    args = parser.parse_args()
    
    if args.password:
        db.create_tables(sha256_crypt.encrypt(args.password))
    
    logging.info('Starting server')
    server.run()

if __name__ == '__main__':
    main()
