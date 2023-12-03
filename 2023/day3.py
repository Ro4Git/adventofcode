#Advent of code 2023: Day 3
#https://adventofcode.com/2023/day/3
import re, time, copy

f = open('input_day3.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

maxWidth = len(lines[0])
maxHeight = len(lines)

numbers = []
# find all numbers and their position in the grid 
# result array of [Number, Line, (xStart,xEnd)]
for i,line in enumerate(lines):
   matches = re.finditer(r"\d+",line)
   for match in matches:
       numbers.append([int(match[0]),i,match.span()])
       
def checkIfSymbolAround(num):
    value = num[0]
    yStart = max(0,num[1]-1)
    yEnd = min(num[1]+2,maxHeight)
    xStart = max(0,num[2][0]-1)
    xEnd = min(num[2][1]+1,maxWidth)
    for y in range(yStart,yEnd):
        for x in range(xStart,xEnd):
            c = lines[y][x]
            if (not c.isdigit() and c!='.'):
                return value
    return 0


def part1():
    totalSum = sum([checkIfSymbolAround(n) for n in numbers])
    print(totalSum)
    return 

def findGearOccurence(s):
    return [i for i, c in enumerate(s) if c == '*']

def checkNumbersAroundGear(x,y):
    numsAround = []
    for n in numbers:
        if ((y>=n[1]-1) and (y<=n[1]+1) and (x>=n[2][0]-1) and (x<=n[2][1])):
            numsAround.append(n)
    if len(numsAround) == 2:
        return numsAround[0][0]*numsAround[1][0]
    return 0



def part2():
   totalSum = 0
   for y,line in enumerate(lines):
       for x in findGearOccurence(line):
            totalSum += checkNumbersAroundGear(x,y)
   print(totalSum)
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