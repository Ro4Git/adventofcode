#Advent of code 2021: Day 12
#https://adventofcode.com/2021/day/12
import re, time, copy, math
from collections import defaultdict

f = open('input_day12.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

graph = defaultdict(list)
allPaths = []
for line in lines:
    tokens = line.split('-')
    graph[tokens[0]].append(tokens[1])
    graph[tokens[1]].append(tokens[0])


def openNode(a,path,duplicate):
    global allPaths
    if a == "end":
        allPaths.append(path)
        return
    for n in graph[a]:
        if n.islower() and n in path:
            if n != "start" and duplicate == "":
                npath = path + [n]
                openNode(n,npath,n)
        else:
            npath = path + [n]
            openNode(n,npath,duplicate)


def part1():
    print(graph)
    openNode("start",["start"],"skip")
    print(len(allPaths))
    return

def part2():
    global allPaths
    allPaths= []
    openNode("start",["start"],"")
    print(len(allPaths))
    return

print("----- Part1 ----")
startp1 = time.time()
part1()
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part2()
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))