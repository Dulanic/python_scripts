import psycopg2
from decouple import config

pguser = config('pguser')
pgpass = config('pgpass')

# Connect to your postgres DB
# file deepcode ignore MissingClose: <please specify a reason of ignoring this>
conn = psycopg2.connect(dbname="bills", user=pguser,
                        password=pgpass, host="192.168.2.155")

# Open a cursor to perform database operations
cur = conn.cursor()