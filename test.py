db_host = 'localhost'
db_name = 'Test'
db_user = 'postgres'
db_pass = '1234'


from ast import Try
from sqlite3 import Cursor
import psycopg2
from reader import *

def create_Author_table():
    """ create a Author table if not exist """
    sql_create_table = """CREATE TABLE IF NOT EXISTS Authors ( 
                Author_ID SERIAL PRIMARY KEY,
                Author_Name varchar(300) NOT NULL UNIQUE,
                UNIQUE (Author_Name)
                )    """
    conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
    cursor = conn.cursor()
    cursor.execute(sql_create_table)
    conn.commit()   
    conn.close()  

def Insert_into_Authors(names):
    """Insert author names (names is a list) into authors table"""
    insert="""INSERT INTO Authors(Author_Name)
                VALUES(%s)
                ON CONFLICT (Author_Name) DO NOTHING
                RETURNING Author_ID """
    conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
    cursor = conn.cursor()
    for name in names:
        cursor.execute(insert,(name,))


    """ #Author_ID = cursor.fetchone()[0]
    #print(Author_ID)
    try:
      Author_ID = cursor.fetchone()[0]
      if (Author_ID):
        print(Author_ID)
    except:
        print('duplicate value') """
     
    conn.commit() 
    conn.close()


#create author table
create_Author_table()

#read authors from source file
Authors=read_authors()

#insert authors in authors table
Insert_into_Authors(Authors)



#conn.close()

