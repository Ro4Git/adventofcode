#Advent of code 2023: Day 4
#https://adventofcode.com/2023/day/4
import re, time, copy

f = open('input_day4.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

numbers = []
startIndexWinNumbers = 10
startIndexMyNumbers = 42
numWinNumbers = 10
numMyNumbers = 25

for line in lines: 
    winNumbers = [int(line[startIndexWinNumbers+i*3:startIndexWinNumbers+2+i*3]) for i in range(numWinNumbers)]
    myNumbers = [int(line[startIndexMyNumbers+i*3:startIndexMyNumbers+2+i*3]) for i in range(numMyNumbers)]
    numbers.append([winNumbers,myNumbers])
#print(numbers)

def part1():
    points = 0
    for winN,myN in numbers:
        winCount = len([n for n in myN if n in winN])
        if winCount:
            points += 2 ** (winCount - 1)
    print(points)
    return 


winCounts = []
gainCards = [0]*len(lines)

def wonCards(index):
    global gainCards
    #bounds?
    if index >= len(winCounts):
        return 0
    #already processed?
    if gainCards[index]:
        return gainCards[index]
    
    totalScratchCard = 1
    winCount = winCounts[index]
    #recurse 
    for i in range(winCount):
        totalScratchCard += wonCards(index + i + 1)
    gainCards[index] = totalScratchCard
    return totalScratchCard


def part2():
    global winCounts
    winCounts = [len([n for n in myN if n in winN]) for  winN,myN in numbers]
    totalcards = sum([wonCards(i) for i in range(len(winCounts))])
    print(totalcards)
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