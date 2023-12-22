#Advent of code 2023: Day 19
#https://adventofcode.com/2023/day/19
import re, time, copy, math, numpy
import json

f = open('input_day19.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()


workflows = {}
parts = []
readingWorkflow = True
for line in lines: 
    if line == "":
        readingWorkflow = False
        continue
    if readingWorkflow:
        strings = line.split("{")
        workName = strings[0]
        rules = strings[1][:-1].split(",")
        workflows[workName] = rules
    else:
        result = re.search("\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}",line)
        part = {} 
        part["x"] = int(result.group(1))
        part["m"] = int(result.group(2))
        part["a"] = int(result.group(3))
        part["s"] = int(result.group(4))
        parts.append(part) 

print(workflows)
print(parts)

def processPart(part,workName):
    workflow = workflows[workName]
    for rule in workflow:
        if ":" in rule: 
            condition,result = rule.split(":")
            value = part[condition[0]]
            testValue = 0
            conditionMet = False
            if "<" in rule:
                testValue = int(condition.split("<")[1])
                conditionMet = value < testValue
            else: 
                testValue = int(condition.split(">")[1])
                conditionMet = value > testValue
            if (conditionMet):
                if result == "R":
                    return False
                elif result == "A":
                    return True
                else:
                    return processPart(part,result)
        elif rule == "A":
            return True
        elif rule != "R":
            return processPart(part,rule)
        else: 
            return False
    return 

def validInRange(ranges):
    return math.prod([(1 + r[1] - r[0]) for r in ranges.values()])

def processRange(ranges,workName):
    totalValid = 0
    workflow = workflows[workName]
    for rule in workflow:
        if ":" in rule: 
            condition,result = rule.split(":")
            partCode = condition[0]
            value = part[partCode]
            newRanges = copy.deepcopy(ranges)
            if "<" in rule:
                testValue = int(condition.split("<")[1])
                if newRanges[partCode][0] < testValue:
                    newRanges[partCode][1] = min(newRanges[partCode][1], testValue-1)
                ranges[partCode][0] = max(ranges[partCode][0] , testValue)
            else: 
                testValue = int(condition.split(">")[1])
                if newRanges[partCode][1] > testValue:
                    newRanges[partCode][0] = max(newRanges[partCode][0], testValue+1)
                ranges[partCode][1] = min(ranges[partCode][1] , testValue)
            if result == "A":
                totalValid += validInRange(newRanges)
            elif result != "R":
                totalValid += processRange(newRanges,result)
        elif rule == "A":
            totalValid += validInRange(ranges)
        elif rule != "R":
            totalValid += processRange(ranges,rule)
    return totalValid


def part1():
    totalSum = 0
    for part in parts:
        if (processPart(part,"in")):
            totalSum += sum(part.values())
    print(totalSum)
    return 

def part2():
    ranges = {"x":[1,4000],"m":[1,4000],"a":[1,4000],"s":[1,4000]}
    totalSum = processRange(ranges,"in")
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