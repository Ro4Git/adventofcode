#Advent of code 2023: Day 5
#https://adventofcode.com/2023/day/5
import re, time, copy

f = open('input_day5.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

# read initial seeds
seeds = [int(n) for n in lines[0][7:].split(" ")]
print(seeds)

#read all maps 
allMaps = []
currentMap = []
lineIndex = 3
while lineIndex < len(lines):
    line = lines[lineIndex]
    if (line == ""):
        # new block
        allMaps.append(currentMap.copy())
        currentMap = []
        lineIndex = lineIndex + 2
    else: 
        currentMap.append([int(n) for n in line.split(" ")])
        lineIndex = lineIndex + 1
    
    if lineIndex >= len(lines):
        allMaps.append(currentMap.copy())
        
print(allMaps)

def convList(inputs, conversionMap):
    output = []
    for n in inputs: 
        found =False
        for map in conversionMap:
            if n>= map[1] and n<map[1]+map[2]:
                res = map[0] + n - map[1]
                output.append(res)
                found = True 
                break
        if not found:
            output.append(n) 

    return output


def convListPart2(inputs, conversionMap):
    output = []
    toProcess = inputs.copy()
    while len(toProcess):
        item = toProcess.pop(0)      
        n = item[0]
        nrange = item[1]
        found =False
        for map in conversionMap:
            destStart = map[0]
            srcStart = map[1]
            destrange = map[2]
            
            if not (n+nrange-1<srcStart or n>= srcStart+destrange):
                #overlapping range
                start = destStart + max(n,srcStart) - srcStart
                end = destStart + min(n+nrange,srcStart+destrange) - srcStart
                output.append( (start , end-start) )                

                #also add remaining parts from source that were not mapped!!!
                if n < srcStart:
                    toProcess.append((n,srcStart - n))
                if n+nrange > srcStart+destrange:
                    toProcess.append( (srcStart+destrange , (n+nrange) - (srcStart+destrange)) )
                found = True 
                break
        if not found:
            output.append((n , nrange)) 

    return output




def part1():
    input = seeds.copy()
    for map in allMaps:
        input = convList(input,map).copy()
    print(input)
    print(min(input))
    return 

def part2():
    input = [(seeds[i],seeds[i+1]) for i in range(0,len(seeds),2)]  
    print(input)
    for map in allMaps:
        input = convListPart2(input,map).copy()
    print(input)
    
    locations = [i[0] for i in input]            
    print(min(locations))
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