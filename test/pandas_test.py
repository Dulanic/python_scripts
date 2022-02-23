import numpy as np
import pandas as pd
import psycopg2
import psycopg2.extras as extras
import sys
from os import walk
import os

mypath = '/home/dulanic/rock'
table = 'list'

files = []
for (dirpath, dirnames, filenames) in walk(mypath):
    files.extend(filenames)
    break

# Connection parameters
params_dic = {"host"      : "192.168.2.155","database"  : "bills", "user"      : "dulanic", "password"  : "bn258090postgres"}

""" Connect to the PostgreSQL database server """
conn = None
try:
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params_dic)
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    sys.exit(1)
print("Connection successful")

for fl in files:
    csv_file = mypath + "/" + fl
    """
    Load and prepare the dataframe for insertion
    into the database, split into chunks
    """
    print(f'Loading {fl} to dataframe.....')

    df = pd.read_csv(csv_file,header=None,sep='\t')
    print(f'Loading {fl} complete')

    # Run the execute_many strategy
    print(f'Loding {csv_file} to database.' )
    """
    Using psycopg2.extras.execute_values() to insert the dataframe
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = 'password'
    # SQL quert to execute
    query  = "INSERT INTO %s(%s) VALUES %%s on conflict do nothing" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
    print("execute_values() done")
    cursor.close()
    print(f"Deleted {csv_file}")
    os.remove(csv_file )


conn.close()


