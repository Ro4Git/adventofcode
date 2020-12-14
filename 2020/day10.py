#Advent of code 2020: Day 10
#https://adventofcode.com/2020/day/10
import time

f = open('input_day10.txt', 'r')
lines = f.readlines()
f.close()

values = [int(n) for n in lines]

joltDevice = max(values) + 3
print(joltDevice)

availableAdapters = [0]*(joltDevice+1)
nbways = [0]*(joltDevice+1)
for n in values:
    availableAdapters[n] = 1
availableAdapters[joltDevice] = 1
availableAdapters[0] = 1
nbways[0] = 1

def part1():
    currentJolt = 0
    nbDif = [0,0,0,0]
    while currentJolt != joltDevice:
        wasJolt = currentJolt
        for i in range(1,4):
           if (availableAdapters[currentJolt + i]):
               currentJolt = currentJolt+i
               nbDif[i] += 1
               break
        if currentJolt == wasJolt:
            print("Not Found!")
            break
    print(nbDif, nbDif[1] * nbDif[3])

def nbWaysToReach(index):
    if not availableAdapters[index]:
        return 0
    nb = 0
    for i in range(1,4):
        if index-i >= 0 and availableAdapters[index-i] != 0:
            nb += nbways[index-i]
    return nb

def part2():
    for i in range(1,joltDevice+1):
        nbways[i] = nbWaysToReach(i)
    print(nbways[joltDevice])

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