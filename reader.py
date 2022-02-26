
from itertools import count
from turtle import title


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
        print(line.removeprefix('#*'))
    elif line.startswith('#@'):
        authors=line.count(',')
        print(line.removeprefix('#@'))
    elif line.startswith('#t'):
        print(line.removeprefix('#t'))
    elif line.startswith('#c'):
        print(line.removeprefix('#c'))
    elif line.startswith('#index'):
        print(line.removeprefix('#index'))
        index+=1

source_file.close()
output_file.close()
    
    