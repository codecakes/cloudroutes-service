import sys
import yaml
import time

from werkzeug.security import generate_password_hash
import rethinkdb as r

from rethinkdb.errors import RqlRuntimeError, RqlDriverError

from runbookdb import RunbookDB

if len(sys.argv) != 2:
    print("Hey, thats not how you launch this...")
    print("%s <config file>") % sys.argv[0]
    sys.exit(1)

# Open Config File and Parse Config Data
configfile = sys.argv[1]

with open(configfile, 'r') as cfh:
    config = yaml.safe_load(cfh)

# Establish Connection
database = config['rethink_db']

db=RunbookDB(configfile)
conn=db.connect()


uid = 'uid_1'

reactiondata = {
    "data": {
        "call_on":  "false" ,
        "extra_headers":  "" ,
        "frequency": 100000 ,
        "http_verb":  "GET" ,
        "name":  "my_reaction" ,
        "payload":  "" ,
        "trigger": 1 ,
        "url": "http://google.com",
        } ,
    "frequency": 100000 ,
    "id":  "rid_1" ,
    "lastrun": 0 ,
    "name":  "my_reaction" ,
    "rtype":  "http" ,
    "trigger": 1 ,
    "uid":  uid
    }

# Add Dummy User
r.db(database).table('reactions').insert([reactiondata]).run(conn)

# Output Data
cursor = r.db(database).table('reactions').run(conn)
for user in cursor:
    print user

# Remove Data
# r.db(database).table('users').delete().run(conn)

# Close Connection
conn.close()

print 'Sample Reaction Added!'
