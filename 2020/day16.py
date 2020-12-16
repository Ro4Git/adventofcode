#Advent of code 2020: Day 16
#https://adventofcode.com/2020/day/16
import re,sys
import time
from functools import reduce


f = open('input_day16.txt', 'r')
lines = f.readlines()
f.close()

def readNumbers(line):
    return [int(nums) for nums in line.split(',')]
    

rules = {}
ranges = []
yourTicket =[]
nearbyTickets =[]

line = lines[0]
currentLine = 0
while line != "\n":
    m = re.search('(.+)\: (\d+)\-(\d+) or (\d+)-(\d+)', line)
    range1 = (int(m.groups()[1]),int(m.groups()[2]))
    range2 = (int(m.groups()[3]),int(m.groups()[4]))
    ranges.append(range1)
    ranges.append(range2)
    rules[m.groups()[0]] = [range1,range2]
    currentLine += 1
    line = lines[currentLine]

currentLine += 1
line = lines[currentLine]
if line != "your ticket:\n":
    print("problem expecting your ticket")
line = lines[currentLine+1]
yourTicket = readNumbers(line)
currentLine +=3
line = lines[currentLine]
if line != "nearby tickets:\n":
    print("problem expecting nearby tickets:")
for line in lines[currentLine+1:]:
    nearbyTickets.append(readNumbers(line))


def checkAgainstpossibleFields(val,ranges):
    return (ranges[0][0] <= val <= ranges[0][1]) or (ranges[1][0] <= val <= ranges[1][1])

def checkAgainstAllRanges(val):
    for min,max in ranges:
        if min <= val <= max:
            return True
    return False

def part1():
    sum = 0
    ticketsToKeep = []
    for ticket in nearbyTickets:
        toRemove = False        
        for val in ticket:
            if not checkAgainstAllRanges(val):
                toRemove = True
                sum += val
        if (not toRemove):
            ticketsToKeep.append(ticket)
    print(sum)
    return ticketsToKeep
    

def part2():
    possibleFields = [[]]*len(yourTicket) 
    #find all possible categories for each ticket number 
    for i in range(len(yourTicket)):
        possibleFields[i] = []
        for k,v in rules.items():
            validpossibleField = True
            for ticket in nearbyTickets:
                if not checkAgainstpossibleFields(ticket[i],v):
                    validpossibleField = False
                    break
            if validpossibleField:
                possibleFields[i].append(k)
    lens = [len(x) for x in possibleFields]
    print(lens)

    #reduce list of possibles for each possibleFields
    while True: 
        for c in possibleFields: 
            if len(c) == 1:
                #remove all occurrence in others
                for c2 in possibleFields: 
                    if (len(c2) > 1):
                        try:
                            c2.remove(c[0])
                        except:
                            len(c2)   
        totalPossibleFields = reduce(lambda x,y : x + len(y), possibleFields, 0)
        if (totalPossibleFields == len(possibleFields)):
            break;

    mul = 1
    for i,cat in enumerate(possibleFields):
        if cat[0].startswith("departure"):
            mul = mul * yourTicket[i]
    print(possibleFields)
    print(mul)



print("----- Part1 ----")
startp1 = time.time()
nearbyTickets = part1()
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part2()
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))

