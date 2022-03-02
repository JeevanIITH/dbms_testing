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
    

    """ #tries to get ids and return ids list
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
        print("Unable to fetch authors ids") """



def Create_ResearchPaper_Table():
    """Create research paper if not exist"""
    sql= """ CREATE TABLE IF NOT EXISTS ResearchPapers(
                Index bigint PRIMARY KEY,
                Title TEXT ,
                Abstract TEXT,
                Main_Author TEXT,
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


def Insert_rp(Rp_attributes):
    """Insert data into rp table """
    sql= """INSERT INTO ResearchPapers(Index,Title,Abstract,Main_Author)
            VALUES(%s,%s,%s,%s) 
            ON CONFLICT(Title) DO NOTHING """
    
    conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
    cursor = conn.cursor()

    for rp in Rp_attributes:
        cursor.execute(sql,(rp[0],rp[1],rp[2],rp[3],))
    conn.commit()
    conn.close()
    
        #print("Error in inserting data into rp")


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

def create_co_author():
    """ create co authors research paper"""
    sql ="""CREATE TABLE IF NOT EXISTS Rp_coAuthors(
            index bigint,
            co_author TEXT,
            UNIQUE (index,co_author)
              )"""
    try:
        conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except:
        print("Unable to create co_Authors")

def insert_coAuthors(co_authors):
    """insert coAuthors"""
    sql="""INSERT INTO  Rp_coAuthors(index,co_author)
            VALUES(%s,%s)
            ON CONFLICT(index,co_author) DO NOTHING"""
    try:
        conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
        cursor = conn.cursor()
        for a in co_authors:
            for b in a[1]:
                cursor.execute(sql,(a[0],b,))
        conn.commit()
        conn.close()
    except:
        print("Unable to insert into co_Authors")

#create author table
#create_Author_table()


#create research paper table
Create_ResearchPaper_Table() 

#create rp authors relation 
#create_Rp_Authors()

create_co_author()


try:
    source_file= open('source.txt','r',encoding="utf8")
    output_file = open('output.txt','w')
except:
    print("Unable to open source.txt file")

Rp_attributes=[]
Authors=[]

co_authors=[]
Rp_author_attr=[]
for i in range(629814):
    index,Title,Author,abstract=read_RpAuthors(source_file)
    #Insert_rp(index,Title,abstract,Author[0])
    tuple = (index,Title,abstract,Author[0])
    Rp_attributes.append(tuple)
    co_author_tuple=(index,Author[1:])
    co_authors.append(co_author_tuple)

    

Insert_rp(Rp_attributes)
insert_coAuthors(co_authors)

source_file.close()



#conn.close()

""" 
co_author_tuple=(index,Author[1:])
co_authors.append(co_author_tuple)
"""
#Authors.append(Author)
#Insert_into_Authors(Author)
""" for id in author_ids:
    print(id) """
#Insert_Rp_Authors(author_ids,index)
