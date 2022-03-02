
from itertools import count
from pickle import TRUE
from turtle import title
from wsgiref.util import FileWrapper


flag=False
#reads all details of the source file and identifies the category
def read_all_details():
    try:
        source_file= open('source.txt','r',encoding="utf8")
        output_file = open('output.txt','w')
    except:
        print("Unable to open source.txt")
        return
    #This number is just for testing , in practice we will import this from file
    counter=629814
    title_counter=0
    authors=0
    index=0
    count_=0
    while counter>0:
        count_+=1
        line = source_file.readline()
        if not line:
            counter-=1
            continue
        if line.startswith('#*'):
            title_counter+=1
            print(f"Title: {line.removeprefix('#*')}")
        elif line.startswith('#@'):
            authors+=line.count(',') + 1
            print(f"Authours are {line.removeprefix('#@')}")
        elif line.startswith('#t'):
            print(f"year : {line.removeprefix('#t')}")
        elif line.startswith('#c'):
            print(f"Paper cited : {line.removeprefix('#c')}")
        elif line.startswith('#index'):
            print(f"ID : {line.removeprefix('#index')}")
            index+=1
        elif line.startswith('#!'):
            print(f"Abstract : { line.removeprefix('#!')  }")

    print(f"No of lines is {count_} \n index is {index} \n Authors : {authors} \n Title : {title_counter} \n ")
    source_file.close()
    output_file.close()


#Identify, read and return (some authors only upto now ) details of the authors
def read_authors():
    try:
        source_file= open('source.txt','r',encoding="utf8")
        output_file = open('output.txt','w')
    except:
        print("Unable to open source.txt file")
    counter=629814
    authors=0
    Authors=[]
    
    while counter>0:
        Author=[]
        line = source_file.readline()
        if  line=='\n':
            counter-=1
            #print(f"counter : {counter}")
            continue
        if line.startswith('#@'):
            authors+=line.count(',') + 1
            #print(f"Authours are {line.removeprefix('#@')}")
            line=line.removeprefix('#@')
            Author=line.split(',')
            Authors.extend(Author)       
    source_file.close()
    output_file.close()
    return Authors

#return a single paper ( Index , Title , Author , abstract) on a call 
def read_RpAuthors(source_file):
    Authors=[]
    line = source_file.readline()
    Author=[]
    abstract=' '
    paper_cited=[]
    while line !='\n' :
        if line.startswith('#*'):
            #title_counter+=1
            #print(f"Title: {line.removeprefix('#*')}")
            line= line.removeprefix('#*')
            Title=line
        elif line.startswith('#@'):
            #authors+=line.count(',') + 1
            #print(f"Authours are {line.removeprefix('#@')}")
            line= line.removeprefix('#@')
            Author=line.split(',')
        elif line.startswith('#index'):
            #print(f"ID : {line.removeprefix('#index')}")
            line = line.removeprefix('#index')
            index=line
        elif line.startswith('#!'):
            #print(f"Abstract : { line.removeprefix('#!')  }")
            line = line.removeprefix('#!')
            abstract = line
        elif line.startswith('#%'):
            line = line.removeprefix('#%')
            paper_cited.append(line)

        line = source_file.readline()
    if(len(Author)==0):
        Author.append('NULL')
    if(len(paper_cited)==0):
        paper_cited.append('NULL')
    return index,Title,Author,abstract,paper_cited

def file_opener():
    try:
        source_file= open('source.txt','r',encoding="utf8")
        output_file = open('output.txt','w')
        return source_file
    except:
        print("Unable to open source.txt file")       

if __name__=="_main_":
    Authors=read_authors()
    print(len(Authors))
    for a in Authors:
        if(a=='\n'):
            print("new line\n")
        print(a)