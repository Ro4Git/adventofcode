#Advent of code 2020: Day 7
#https://adventofcode.com/2020/day/7
import re, time, copy

f = open('input_day7.txt','r')
lines = f.readlines()
f.close()

contains = {}
for line in lines:
    g = re.search("(.*) bags contain (.*)\.",line)
    parentbag = g.groups()[0]
    childrenstr = g.groups()[1].split(", ")
    children = []
    for child in childrenstr:
        g2 = re.search("(\d) (.*) bag",child)
        if (g2):
            count = int(g2.groups()[0])
            color = g2.groups()[1]
            children.append((color,count))
    contains[parentbag] = children        

iscontained = {}
for key,value in contains.items():
    for child in value:
        if (child[0] in iscontained):
            iscontained[child[0]].append((key,child[1]))
        else:
            iscontained[child[0]] = [(key,child[1])]

alreadyparsed = {}

def canContain(bagcolor):
    if (bagcolor in alreadyparsed):        
        return 0
    alreadyparsed[bagcolor] = 1
    if (not bagcolor in iscontained):
        return 1
    count = 1
    for container,nb in iscontained[bagcolor]:
        count += canContain(container)
    return count


def Contains(bagcolor):
    count = 1
    for subbag,nb in contains[bagcolor]:
        print (nb,subbag)
        count += nb * Contains(subbag)
    return count    

def part1():
    nbpossible = canContain("shiny gold")
    print(nbpossible-1)

def part2():
    nbpossible = Contains("shiny gold")
    print(nbpossible-1)

alreadyparsed = {}
print("----- Part1 ----")
startp1 = time.time()
part1()
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

alreadyparsed = {}
print("----- Part2 ----")
startp2 = time.time()
part2()
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))

