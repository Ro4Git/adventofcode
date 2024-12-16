#Advent of code 2024: Day 11
#https://adventofcode.com/2024/day/11
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day11.txt")
seq = [int(c) for c in lines[0].split(" ")]
print(seq)

class CacheItem:
    def __init__(self , data = [], count = 1):
        self.data = data
        self.count = count    
        
    def Hit(self, count = 1):
        self.count += count

def processNumber(cache, n, nbOccurrences):
    if n in cache:
        cache[n].Hit(nbOccurrences)
    else:
        if n== 0:
            cache[n] = CacheItem([1], nbOccurrences)
        else:
            strn = str(n)
            lens = len(strn)
            if (lens & 1) == 0:
                cache[n] = CacheItem([int(strn[:lens//2]),int(strn[lens//2:])],nbOccurrences)
            else:
                cache[n] = CacheItem([n*2024],nbOccurrences)

def initCache(seq):
    currentCache = defaultdict(CacheItem)
    for i,n in enumerate(seq): 
        currentCache[i] = CacheItem([n],1)
    return currentCache            

def processSequence(inputCache):
    currentCache = defaultdict(CacheItem)
    for item in inputCache.values(): 
        for n in item.data:
            processNumber(currentCache,n,item.count)
    return currentCache


def part1():
    input = initCache(seq)
    for i in range(26):
        input = processSequence(input)
    print(sum([item.count for item in input.values()]))
    return 

def part2():
    input = initCache(seq)
    for i in range(76):
        input = processSequence(input)
    print(sum([item.count for item in input.values()]))
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

