#Advent of code 2020: Day 1
#https://adventofcode.com/2020/day/1
import re, time, copy

f = open('input_day1.txt', 'r')
lines = f.readlines()
f.close()

values = [int(v) for v in lines]

def part1():
    for i,val in enumerate(values):
        for j in range(i+1,len(values)):
                if (values[j] + val == 2020):
                    print (val, values[j])
                    print (val * values[j])
                    return 

def part2():
    for i,val in enumerate(values):
        for j in range(i+1,len(values)):
            for k in range(j+1,len(values)):
                if (values[j] + val + values[k] == 2020):
                    print (val, values[j], values[k])
                    print (val * values[j] * values[k])
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