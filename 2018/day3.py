import re
initial_numbers= []


f = open('input_day3.txt','r')
lines = f.readlines()
f.close()

table = {}

def addTag(dict, key, index): 
    if key in dict:
        dict[key] = (dict[key][0] + 1,dict[key][1])
    else: 
        dict[key] = (1,index)

for line in lines:
    tokens = re.split(': | @ |\n',line)
    id = int(tokens[0].split("#")[1])
    spos = tokens[1].split(",")
    ssize = tokens[2].split("x")
    pos = (int(spos[0]), int(spos[1]))
    size = ( int(ssize[0]), int(ssize[1]))
    
    for y in range(pos[1] , pos[1]+size[1] ) :
        for x in range(pos[0] , pos[0]+size[0] ) :
            p = (x,y)
            addTag(table,p,id)

def part1():
    overlapping_items = {k:v for k,v in table.items() if v[0] >= 2 }
    print(len(overlapping_items))

def doNotOverlap(pos, size):
    for y in range(pos[1] , pos[1]+size[1] ) :
        for x in range(pos[0] , pos[0]+size[0] ) :
            p = (x,y)
            if (table[p][0] > 1):
                 return False
    return True

def part2():
    for line in lines:
        tokens = re.split(': | @ |\n',line)
        id = int(tokens[0].split("#")[1])
        spos = tokens[1].split(",")
        ssize = tokens[2].split("x")
        pos = (int(spos[0]), int(spos[1]))
        size = ( int(ssize[0]), int(ssize[1]))
        if (doNotOverlap(pos,size)):
            print(id)
            return 


part1()
part2()   
        