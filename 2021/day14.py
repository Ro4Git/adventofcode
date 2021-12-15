#Advent of code 2021: Day 14
#https://adventofcode.com/2021/day/14
import re, time, copy, math
from collections import defaultdict

f = open('input_day14.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

code = lines[0]

graph = {}
for line in lines[2:]:
    tokens = line.split(' -> ')
    graph[tokens[0]] = tokens[1]

# brute force approach
def processLines(line):
    result = ""
    for i in range(len(line)-1):
        pair = line[i:i+2]
        insert = graph[pair]
        result += pair[0] + insert
    result += line[-1]
    return result

def part1():
    #brute force
    print(code)
    str = code
    for i in range(10):
        str = processLines(str)

    charCount = defaultdict(int)
    for c in str:
        charCount[c] += 1
    res = max(charCount.values()) - min(charCount.values())
    print(charCount)
    print(res)
    return

# only count the number of pairs 
def processPairs(pairs):
    newpairs = defaultdict(int)
    for k,v in pairs.items():
        insert = graph[k]
        newpairs[k[0]+insert] += v
        newpairs[insert+k[1]] += v
    return newpairs


def part2():
    print(code)
    pairs = defaultdict(int)
    for i in range(len(code)-1):
        pair = code[i:i+2]
        pairs[pair] += 1

    for i in range(40):
        pairs = processPairs(pairs)
  
    #now count all characters 
    charCount = defaultdict(int)
    charCount[code[0]] = 1
    charCount[code[-1]] = 1
    for k,v in pairs.items():
        charCount[k[0]] += v
    
    print(charCount)
    res = max(charCount.values()) - min(charCount.values())
    print(res)


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