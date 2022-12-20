#Advent of code 2022: Day 20
#https://adventofcode.com/2022/day/20
import re, time, copy, functools
from collections import deque

f = open('input_day20.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

temp = [int(line) for line in lines]


def part1():
    rotationList = deque([(value,i) for i,value in enumerate(temp)])
#    print("Before :",rotationList)
    for i,n in enumerate(temp):
        index = rotationList.index((n,i))
        rotationList.remove((n,i))
        rotationList.rotate(-n)
        rotationList.insert(index,(n,i))
#      print(n, "=> ",rotationList)
    print("After :" ,rotationList)

    results = [x for x,i in rotationList]
    index = results.index(0)
    tests = [1000,2000,3000]
    values = [results[(index + n) % len(results)] for n in tests] 
    print(sum(values))
    return


def part2():
    tempPart2 = [t * 811589153 for t in temp]
    rotationList = deque([(value,i) for i,value in enumerate(tempPart2)])
    for run in range(10):
        for i,n in enumerate(tempPart2):
            index = rotationList.index((n,i))
            rotationList.remove((n,i))
            rotationList.rotate(-n)
            rotationList.insert(index,(n,i))
#    print("After :" ,rotationList)

    results = [x for x,i in rotationList]
    index = results.index(0)
    tests = [1000,2000,3000]
    values = [results[(index + n) % len(results)] for n in tests] 
    print(sum(values))    
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
