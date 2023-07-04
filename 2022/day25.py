#Advent of code 2022: Day 25
#https://adventofcode.com/2022/day/25
import re, time, copy, functools,sys
from collections import defaultdict


f = open('input_day25.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

code = {'2':2,'1':1,'0':0,'-':-1,'=':-2}
invCode = {2:"2",1:"1",0:"0",-1:"-",-2:'='}

def add(str1,str2):
    res = []
    index1 = len(str1)-1
    index2 = len(str2)-1
    ret = 0
    while index1 >= 0 or index2>=0:
        c1 = code[str1[index1]] if index1>=0 else 0
        c2 = code[str2[index2]] if index2>=0 else 0
        newC = c1 + c2 + ret
        ret = 0
        if newC > 2:
            ret = 1 
            newC = newC-5
            res.append(invCode[newC])
        elif newC <- 2:
            newC = newC +5 
            ret = -1 
            res.append(invCode[newC])
        else:
            res.append(invCode[newC])
        index1 -= 1
        index2 -= 1
    if ret:
        res.append("1")

    return "".join(reversed(res))
         
def part1():
    str = "1"
    for i in range(20):
        str = add(str,"1")
        print(str)

    part1res= "0"
    for line in lines:
        part1res = add(part1res,line)
        print(part1res)
    print(part1res)
    return 



def part2():
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
