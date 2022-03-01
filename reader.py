
from itertools import count
from turtle import title



def read_all_details():
    source_file= open('source.txt','r')
    output_file = open('output.txt','w')
    counter=3
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
    
def read_authors():
    try:
        source_file= open('source.txt','r',encoding="utf8")
        output_file = open('output.txt','w')
    except:
        print("Unable to open source.txt file")
    counter=20
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


if __name__=="_main_":
    Authors=read_authors()
    print(len(Authors))
    for a in Authors:
        if(a=='\n'):
            print("new line\n")
        print(a)