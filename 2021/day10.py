#Advent of code 2021: Day 10
#https://adventofcode.com/2021/day/10
import re, time, copy, functools

f = open('input_day10.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

closingChar = {'{':'}','[':']','(':')','<':'>'}
errorPoints = {'}':1197,']':57,')':3,'>':25137}
completionPoint = {'}':3,']':2,')':1,'>':4}

totalPart2Points=[]
totalPart1Points = 0
global validLines
for line in lines:
    openedChunks = []
    part1Points = 0
    for c in line:
        if c in closingChar.keys():
            openedChunks.append(c)
        else:
            expected = closingChar[openedChunks[-1]]
            if (expected != c):
                # print(line + "-  expected " + expected + ", but found " + c + "instead.")
                part1Points = errorPoints[c]
                break
            else:
                openedChunks.pop()
    if part1Points > 0:
        totalPart1Points += part1Points
    else:
        #incomplete line, remaining character are the
        openedChunks.reverse()
        missingChars = [closingChar[c] for c in openedChunks]
        # print("Missing chars: " + str(missingChars))
        part2points = functools.reduce(lambda a,b:a*5+completionPoint[b],missingChars,0)
        totalPart2Points.append(part2points)


def part1():
    print("Part1 :" + str(totalPart1Points))
    return

def part2():
    print("Part2 :" )
    totalPart2Points.sort()
    print(totalPart2Points[len(totalPart2Points)//2])

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