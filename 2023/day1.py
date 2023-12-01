#Advent of code 2023: Day 1
#https://adventofcode.com/2023/day/1
import re, time, copy

f = open('input_day1.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

nbs = ["one","two","three","four","five","six","seven","eight","nine"]

def part1():
    nums = []
    for line in lines: 
        digits = [c for c in line if c.isdigit()]
        res = digits[0] + digits[-1]
        nums.append(int(res))
    print(nums)
    print(sum(nums))
    return 

def part2():
    nums = []
    for line in lines: 
        digits = []
        for i,c in enumerate(line): 
            if c.isdigit():
                digits.append(c)
            else:
               for j,n in enumerate(nbs):
                   if i + len(n) <= len(line):
                       test = line[i:i+len(n)]
                       if (test == n):
                           digits.append(str(j+1))
                           break
        res = digits[0] + digits[-1]
        nums.append(int(res))
    print(nums)
    print(sum(nums))

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