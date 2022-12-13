#Advent of code 2022: Day 3
#https://adventofcode.com/2022/day/3
import re, time, copy

f = open('input_day3.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

def commonChar(s1,s2):
    for c in s1: 
        if c in s2: 
            return c
    return ''

def commonChar3(s1,s2,s3):
    for c in s1: 
        if c in s2: 
            if c in s3: 
                return c
    return ''

def prio(c):
    if (ord(c) > ord('a')): 
        return 1 + ord(c) - ord('a')
    else:
        return 27+ ord(c) - ord('A')

def part1():
    commonChars = [commonChar(line[:len(line)//2],line[len(line)//2:]) for line in lines]
    sumPrios = sum([prio(c) for c in commonChars])
    print(sumPrios)
    return 

def part2():
    badges =[commonChar3(lines[i],lines[i+1],lines[i+2]) for i in range(0,len(lines),3)] 
    sumPrios = sum([prio(c) for c in badges])
    print(sumPrios)
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