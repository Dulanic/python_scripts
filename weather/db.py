import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

pguser = os.environ.get('pguser')
pgpass = os.environ.get('pgpass')

# Connect to your postgres DB
conn = psycopg2.connect(dbname="bills", user=pguser,
                        password=pgpass, host="192.168.2.155")

# Open a cursor to perform database operations
cur = conn.cursor()