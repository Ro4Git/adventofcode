#Advent of code 2020: Day 3
#https://adventofcode.com/2020/day/3
import re, time, copy

f = open('input_day3.txt','r')
lines = f.readlines()
f.close()


slopes = [(1,1),(3,1),(5,1),(7,1),(1,2)]

lineLength = len(lines[0])-1
print(lineLength, len(lines))

def countTree(slopeX,slopeY):
    nbTree = 0
    pos = 0
    posy = 0

    for i,line in enumerate(lines):
        if (i == posy):
            if (line[pos] == '#'):
                nbTree += 1
            pos = pos + slopeX
            pos = pos % lineLength
            posy += slopeY
    print(nbTree)
    return nbTree

def part1():
    print(countTree(3,1))

def part2():
    result = 1
    for slope in slopes:
        result *= countTree(slope[0],slope[1])
    print(result)

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