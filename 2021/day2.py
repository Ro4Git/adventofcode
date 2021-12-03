#Advent of code 2021: Day 2
#https://adventofcode.com/2021/day/2
import re, time, copy


f = open('input_day2.txt','r')
lines = f.readlines()
f.close()

directions = {
    "forward": (1,0),
    "down": (0,1),
    "up": (0,-1)
}

startpos = (0,0)

def mulDir(dir, delta):
    return (dir[0]*delta,dir[1]*delta)

def addDir(pos, dir):
    return (pos[0]+dir[0],pos[1]+dir[1])

deltas = [mulDir(directions[token[0]],int(token[1])) for token in [v.split() for v in lines]]


def part1():
    pos = sum(i for i,j in deltas)
    depth = sum(j for i, j in deltas)
    print(pos * depth)


def part2():
    aim = 0
    pos = 0
    depth = 0
    for delta in deltas:
        aim = aim + delta[1]
        pos = pos + delta[0]
        depth = depth + aim * delta[0]
    print(pos * depth)


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