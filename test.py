db_host = 'localhost'
db_name = 'Test'
db_user = 'postgres'
db_pass = '1234'


import psycopg2
conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass)
conn.close()

