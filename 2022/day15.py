#Advent of code 2022: Day 15
#https://adventofcode.com/2022/day/15
import re, time, copy, functools
import pygame
from interval import interval, inf, imath

f = open('input_day15.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()


temp = [re.findall(r"-?\d+",line) for line in lines]
sensors = []

minx = miny = 10000000000
maxx = maxy = -10000000000

for numbers in temp:
    spos = (int(numbers[0]),int(numbers[1]))
    bpos = (int(numbers[2]),int(numbers[3]))
    dist = abs(spos[0] - bpos[0]) + abs(spos[1] - bpos[1])
    sensor = (spos,dist)
    sensors.append(sensor)
    minx = min(minx,spos[0])
    maxx = max(maxx,spos[0])
    miny = min(miny,spos[1])
    maxy = max(maxy,spos[1])

print(minx,miny,maxx,maxy)
width = maxx - minx
height = maxy - miny
print(width,height)

def getInterval(y):
    line = interval()
    for sensor in sensors:
        dist = sensor[1]
        if (sensor[0][1] - dist <= y <= sensor[0][1] + dist):
            intervalSize = dist - abs(sensor[0][1] - y)
            if (intervalSize > 0):
                line = line | interval([sensor[0][0]-intervalSize , sensor[0][0]+intervalSize])
    return line

def getIntervalPart2(y):
    line = interval()
    for sensor in sensors:
        dist = sensor[1]
        if (sensor[0][1] - dist <= y <= sensor[0][1] + dist):
            intervalSize = dist - abs(sensor[0][1] - y)
            if (intervalSize > 0):
                line = line | interval([sensor[0][0]-intervalSize , sensor[0][0]+intervalSize])
    return line    


def part1():
    #noBeacons = getInterval(2000000)
    noBeacons = getInterval(10)
    print(noBeacons)
    size = 0
    for x in noBeacons.components:
        size += x[0].sup - x[0].inf
    print(size)

    return

def part2():
    maxSize = 4000000
    testInterval = interval([0,maxSize])
    for y in range(maxSize+1):
        if (y % 100000) == 0:
            print(y)
        noBeacons = getInterval(y)
        #is there a free spot between [0,4000000] ?
        intersect = noBeacons & testInterval
        if len(intersect)>1 or intersect != testInterval:
            print(y,intersect)
            for subint in intersect.components:
                x =  subint[0].sup+1
                val = y + x * 4000000
                print(x,y,val)
            return
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

