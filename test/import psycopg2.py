import psycopg2
from csv import reader


	


with open('/home/dulanic/rock/temp/1', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Get all rows of csv from csv_reader object as list of tuples
    list_of_tuples = list(map(tuple, csv_reader))
    # display all rows of csv

  
conn = psycopg2.connect("host='192.168.2.155' port='5432' dbname='bills' user='dulanic' password='bn258090postgres'")
cur = conn.cursor()

args_str = ','.join(cur.mogrify("(%s)", x) for x in list_of_tuples)
cur.execute("INSERT INTO list VALUES " + args_str) 
connection.commit()
count = cursor.rowcount
print (count, "Successfully inserted")