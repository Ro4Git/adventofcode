#Advent of code 2020: Day 18
#https://adventofcode.com/2020/day/18
import re,sys
import time,itertools
from functools import reduce


f = open('input_day18.txt', 'r')
lines = f.readlines()
f.close()


def parenthesisBlock(str):
    parenthesisCount = 1
    #parenthesis block
    endBlock1 = len(str)-2
    while parenthesisCount >0 and endBlock1>=0:
        if str[endBlock1] == "(": 
            parenthesisCount -= 1
        elif str[endBlock1] == ")":
            parenthesisCount += 1
        endBlock1 -= 1
    return str[endBlock1+1:]

def extractBlocks(str):
    if len(str) ==0:
        return ("","","")
    blockR = ""
    blockL = ""
    op = ""
    if str[-1] == ")": 
        blockR = parenthesisBlock(str)
        if (len(str) == len(blockR)):
            return extractBlocks(blockR[1:len(blockR)-1])
        else:
            op = str[len(str) - len(blockR) - 2]
            blockL = str[0:-(len(blockR)+3)]
    else:
        #number #op #anything
        m = re.match("(.*) ([\+\*]) (\d+)",str)
        if len(m.groups()) ==3:
            blockL = m.groups()[0]
            blockR = m.groups()[2]
            op = m.groups()[1]
        else:
            blockR = str
    return (blockL,op,blockR)
    

def evalStringPart1(str):
    if (len(str) == 0):
        return 0
    if (len(str) == 1):
        return int(str)
    blockL, op, blockR = extractBlocks(str)
    val1 = 0
    val2 = 0
    if (op != ""):
        val1 = evalStringPart1(blockL)
        val2 = evalStringPart1(blockR)
        if (op == "*"):
            return val1 * val2
        if (op == "+"):
            return val1 + val2
    else:
        return evalStringPart1(blockR)
    

def part1():
    sum = 0 
    print(evalStringPart1("1 + 2 * 3 + 4 * 5 + 6"))
    print(evalStringPart1("1 + (2 * 3) + (4 * (5 + 6))"))
    print(evalStringPart1("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))
    
    for line in lines: 
        val = evalStringPart1(line.rstrip())
        sum += val 
    print(sum)

def part2():
    #went the wrong way with part1 to have part2 easily so went for 
    #this other below
    return 

#----------------------------------------------------------------
# such a better and elegant solution 
# from Ruben Holen using eval()
class Term(int):
    def __mul__(self, other): return Term(int.__mul__(self, other))
    def __add__(self, other): return Term(int.__add__(self, other))
    __sub__ = __mul__
    __pow__ = __add__
exprs = [re.sub(r'(\d+)', r'Term(\1)', line) for line in lines]
print(sum(eval(e.replace('*', '-')) for e in exprs))
print(sum(eval(e.replace('+', '**')) for e in exprs))
#----------------------------------------------------------------


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

