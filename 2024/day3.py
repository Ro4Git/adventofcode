#Advent of code 2024: Day 3
#https://adventofcode.com/2024/day/3
import re, time, copy 
import aoc

lines = aoc.ReadPuzzleInput("input_day3.txt")
line = ''.join(lines)

def part1():
    occurrences =re.findall("mul\((\d+),(\d+)\)",line)
    muls = [int(a)*int(b) for a,b in occurrences]
    print(hex(sum(muls)))
    return 

def part2():
    occurrences = re.findall("do\(\)|don't\(\)|mul\(\d+,\d+\)",line)
    mulEnable= True
    valids = []
    for n in occurrences:
        if n == "don't()":
            mulEnable = False
        elif n == "do()":
            mulEnable = True
        elif mulEnable:
            valids.append(re.findall("mul\((\d+),(\d+)\)",n)[0])

    muls = [int(a)*int(b) for a,b in valids]
    print(sum(muls))
    
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