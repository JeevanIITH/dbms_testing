db_host = 'localhost'
db_name = 'Test'
db_user = 'postgres'
db_pass = '1234'


from ast import Try
from fileinput import close
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
    try:
        conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
        conn.commit()   
        conn.close()  
    except:
        print("Unable to connect to database")
        return
    

def Insert_into_Authors(names):
    """Insert author names (names is a list) into authors table"""
    insert=""" INSERT INTO Authors(Author_Name)
                VALUES(%s)
                ON CONFLICT (Author_Name) 
                DO NOTHING
                RETURNING Author_ID  
              """
    """ Get ids of inserted authors """
    get_id ="""SELECT Author_ID FROM Authors
                WHERE  Author_Name = %s"""

    #tries to insert
    try:            
        conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
        cursor = conn.cursor()
        for name in names:
            cursor.execute(insert,(name,))
            conn.commit()   
    except:
        print("Error in inserting Author into Authors")
    

    #tries to get ids and return ids list
    try:
        conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
        cursor = conn.cursor()
        author_ids=[]
        for n in names:
            cursor.execute(get_id,(n,))
            author_ids.append(cursor.fetchone()[0])
        
        conn.commit() 
        conn.close()
        return author_ids
    except:   
        print("Unable to fetch authors ids")



def Create_ResearchPaper_Table():
    """Create research paper if not exist"""
    sql= """ CREATE TABLE IF NOT EXISTS ResearchPapers(
                Index bigint PRIMARY KEY,
                Title varchar(300) ,
                Abstract TEXT,
                Main_Author varchar(300),
                UNIQUE (Title)
                )"""
    try:
        conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except:
        print("Rp Unable to connect to database")


def Insert_rp(index, title, abstract,main_author):
    """Insert data into rp table """
    sql= """INSERT INTO ResearchPapers(Index,Title,Abstract,Main_Author)
            VALUES(%s,%s,%s,%s) 
            ON CONFLICT(Title) DO NOTHING """
    try:
        conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
        cursor = conn.cursor()
        cursor.execute(sql,(index,title,abstract,main_author,))
        conn.commit()
        conn.close()
    except:
        print("Error in inserting data into rp")


# research paper and its authors relation 
def create_Rp_Authors():
    """create research paper relation """
    sql = """CREATE TABLE IF NOT EXISTS Rp_Authors(
                    Author_ID bigint,
                    RP_Index bigint
                        ) """
    try:
        conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except:
        print("Unable to create Rp_Authors")


def Insert_Rp_Authors(Author_IDs,RP_index):

    """insert into rp_authors"""
    sql = """INSERT INTO Rp_Authors(Author_ID,RP_Index)
              VALUES(%s,%s)  """
    try:
        conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
        cursor = conn.cursor()
        for Author_ID in Author_IDs:
            cursor.execute(sql,(Author_ID,RP_index,))
        conn.commit()
        conn.close()
    except:
        print("Unable to insert data into rp_authors")


#create author table
create_Author_table()


#create research paper table
Create_ResearchPaper_Table() 

#create rp authors relation 
create_Rp_Authors()


try:
    source_file= open('source.txt','r',encoding="utf8")
    flag=True
    output_file = open('output.txt','w')
except:
    print("Unable to open source.txt file")

for i in range(629814):
    index,Title,Author,abstract=read_RpAuthors(source_file)
    Insert_rp(index,Title,abstract,Author[0])
    author_ids=Insert_into_Authors(Author)
    Insert_Rp_Authors(author_ids,index)


source_file.close()



#conn.close()

