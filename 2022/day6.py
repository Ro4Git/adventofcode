#Advent of code 2022: Day 6
#https://adventofcode.com/2022/day/6
import re, time, copy

f = open('input_day6.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

dataStream = lines[0]

def isMarker(str,index,markerLength):
    s = set(str[index:index+markerLength])
    return len(s) == markerLength

def findMarker(markerLength):
    foundIndex = -1
    for i in range(len(dataStream)-markerLength):
        if isMarker(dataStream,i,markerLength):
            print(dataStream[i:i+markerLength])
            foundIndex = i+markerLength
            break
    return foundIndex
    
def part1():
    print(findMarker(4))
    return 

def part2():
    print(findMarker(14))
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