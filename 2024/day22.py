#Advent of code 2024: Day 22
#https://adventofcode.com/2024/day/22
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day22.txt")
numbers = [int(line) for line in lines]

def processNumber(n):
    x = n << 6
    x = x ^ n
    x = x & 16777215 # 2pow 24
    x2 = x >> 5
    x = x ^ x2
    x = x & 16777215 # 2pow 24  
    x3 = x << 11
    x = x ^ x3
    x = x & 16777215 # 2pow 24 
    return x

def process(n , depth):
    result = [n]
    for i in range(depth):
       n = processNumber(n)
       result.append(n)
    return result

buyersSecrets = [process(n,2000) for n in numbers]

def secretsDelta(secrets):
    deltas = {}
    prices = [p%10 for p in secrets]
    for i in range(4,len(prices)):
        seq = (prices[i-3] - prices[i-4] , prices[i-2] - prices[i-3] , prices[i-1] - prices[i-2],  prices[i] - prices[i-1])
        if not seq in deltas:
            deltas[seq] = prices[i]
    return deltas


def part1():
    res = [seq[-1] for seq in buyersSecrets]
    print(sum(res))
    return 

def part2():
    revenues = defaultdict(int)
    for secrets in buyersSecrets:
        buyerDeltas = secretsDelta(secrets)
        for seq,prize in buyerDeltas.items():
             revenues[seq] += prize
    result = max(revenues.values())
    print(result)
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

