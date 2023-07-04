#Advent of code 2022: Day 21
#https://adventofcode.com/2022/day/21
import re, time, copy, functools
from collections import deque

f = open('input_day21.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()


ops = {item[0]: re.split('[ ]+',item[1][1:]) for item in [line.split(":") for line in lines]}

def eval(key):
    op = ops[key]
    if len(op) == 1:
        return int(op[0])
    else:
        if op[1] == "*":
            return eval(op[0]) * eval(op[2])
        elif op[1] == "/":
            return eval(op[0]) / eval(op[2])
        elif op[1] == "+":
            return eval(op[0]) + eval(op[2])
        elif op[1] == "-":
            return eval(op[0]) - eval(op[2])
    print("error?")
    return 0

def part1():
    value = eval("root")
    print(value)
    return

def part2():
    opRoot = ops["root"]
    ops["humn"] = ["2411"]
    vleft = eval(opRoot[0])
    vright = eval(opRoot[2])

    start = -1000000000000000
    end = 1000000000000000
    dist = vleft - vright

    while start != end and dist != 0: 
        mid = (start + end)//2 
        ops["humn"] = [str(mid)]
        vleft = eval(opRoot[0])
        dist = vleft - vright
        print(mid ,"[",start,",",end,"] => ",vleft,vright, vleft - vright)
        if (dist > 0):
            if start == mid:
                start = end
            else:
                start = mid
        elif dist <0:
            if end == mid:
                end = start
            else:
                end = mid
        else:
            print("Found ",mid)
            break
    

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
