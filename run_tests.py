from app import db
import bcrypt

import testsuite


pw = bcrypt.hashpw(str('1234').encode('utf-8'), bcrypt.gensalt())
db.create_tables(pw.decode('utf-8'))
testsuite.run()
