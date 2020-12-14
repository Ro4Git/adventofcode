#Advent of code 2020: Day 6
#https://adventofcode.com/2020/day/6
import re, time, copy

f = open('input_day6.txt','r')
lines = f.readlines()
f.close()

answers=[0]*26
nbingroup = 0
groupspart1 = []
groupspart2 = []
for line in lines:
    line = line.rstrip()
    if (line == ""):    #end of group
        groupspart1.append(sum(1 for i in answers if i>0))
        if (nbingroup>0):
            groupspart2.append(answers.count(nbingroup))
        answers=[0]*26
        nbingroup = 0
    else:
        nbingroup += 1
        for c in line:
            answers[ord(c)-97] += 1       

def part1():
    res = 0
    for g in groupspart1:
        res = res + g
    print(res)       

def part2():
    res = 0
    for g in groupspart2:
        res = res + g
    print(res)       

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