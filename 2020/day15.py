#Advent of code 2020: Day 15
#https://adventofcode.com/2020/day/15
import re,sys
import time

input = [1,20,11,6,12,0]


def updateProgress():
    text = "\rNumbers: {0} Dict({1})".format( len(numbers), len(lastoccurence))
    sys.stdout.write(text)
    sys.stdout.flush()

def part(limit):
    lastoccurence = {}
    for i,v in enumerate(input):
        lastoccurence[v] = i
    spoken = input[-1]
    lastoccurence.pop(spoken)
    lastspoken = 0

    for round in range(len(input), limit):
        lastSpoken = spoken
        spoken = (round-1) - lastoccurence[spoken] if spoken in lastoccurence else 0
        lastoccurence[lastSpoken] = round - 1 
    print(spoken)
    return spoken


print("----- Part1 ----")
startp1 = time.time()
part(2020)
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part(30000000)
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))

#Python
#----- Part1 ----
#436
#0.0010s
#----- Part2 ----
#175594
#19.1146s

#Pypy
#----- Part1 ----
#1085
#0.0020s
#----- Part2 ----
#10652
#4.1444s