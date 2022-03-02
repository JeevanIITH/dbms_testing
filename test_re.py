db_host = 'localhost'
db_name = 'Test'
db_user = 'postgres'
db_pass = '1234'


from ast import Try
from fileinput import close
from sqlite3 import Cursor
import psycopg2
from reader import *




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


def create_paper_cited():
    """create paper cited by table"""
    sql = """CREATE TABLE IF NOT EXISTS paper_cited
            (
                index bigint,
                cited_index TEXT,
                UNIQUE (index,cited_index)
            )
            """
    try:
        conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except:
        print("Unable to create paper_cited table")

def insert_paper_cited(indexes):

    sql = """INSERT INTO paper_cited(index,cited_index)
            VALUES(%s,%s)
            ON CONFLICT(index,cited_index) DO NOTHING
            """
    
    try:
        conn = psycopg2.connect(host = db_host , database = db_name , user = db_user , password = db_pass) 
        cursor = conn.cursor()
        for index in indexes:
            for ind in index[1]:
                cursor.execute(sql,(index[0],ind,))
        conn.commit()
        conn.close()
    except:
        print("Unable to insert into paper cited table")


#----- Creating tables ---------

#create research paper table
Create_ResearchPaper_Table() 

#create rp authors relation 
#create_Rp_Authors()

create_co_author()

create_paper_cited()

#-------opening source file-----------
try:
    source_file= open('source.txt','r',encoding="utf8")
    output_file = open('output.txt','w')
except:
    print("Unable to open source.txt file")


#-------get details to push in to database
Rp_attributes=[]
Authors=[]
co_authors=[]
p_cited_attr=[]


for i in range(629814):
    index,Title,Author,abstract,paper_cited=read_RpAuthors(source_file)
    
    #gathering research paper details in list 
    tuple = (index,Title,abstract,Author[0])
    Rp_attributes.append(tuple)

    #gathering details of co author in list
    co_author_tuple=(index,Author[1:])
    co_authors.append(co_author_tuple)

    #gathering paper cited details in list
    p_cited_tuple=(index,paper_cited)
    p_cited_attr.append(p_cited_tuple)

    

#inserting details into database
Insert_rp(Rp_attributes)
insert_coAuthors(co_authors)
insert_paper_cited(p_cited_attr)

source_file.close()

