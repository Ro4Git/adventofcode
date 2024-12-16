#Advent of code 2024: Day 13
#https://adventofcode.com/2024/day/13
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

class Machine: 
    def __init__(self,data): 
        self.b1 = data[0][0]
        self.b2 = data[1][0]
        self.prize = data[2][0]
    
    def __str__(self):        
        return str(self.__dict__)
    
    def tokenCost(self, delta = 0):  
# solving 
# p(xp,yp) = nbStep1 * b1 + nbStep2 * b2
#
# (1) xp = nbStep1 * b1.x + nbStep2 * b2.x
# (2) yp = nbStep1 * b1.y + nbStep2 * b2.y
#
# eliminate nbStep2 => b2.y*(1) - b2.x*(2) 
#  =>  b2.y * xp - b2.x * yp = nbStep1 ( b1.x * b2.y - b1.y * b2.x)
# nbStep1 =   (b2.y * xp - b2.x * yp) / ( b1.x * b2.y - b1.y * b2.x)
#
# eliminate nbStep1 => b1.y*(1) - b1.x*(2) 
# =>  b1.y * xp - b1.x * yp = nbStep2 ( b2.x * b1.y - b2.y * b1.x)
# nbStep2 = - (b1.y * xp - b1.x * yp) / ( b1.x * b2.y - b1.y * b2.x) 
        
        nprize = aoc.addPos(self.prize, (delta,delta))
        det = aoc.crossPos2(self.b1, self.b2)
        if det == 0: 
            return 0 # 0 means impossible (b1 / b2 are parralel)
        num1 = aoc.crossPos2(nprize,self.b2)
        num2 = -aoc.crossPos2(nprize,self.b1)
        nbStep1,rem1 = divmod(num1,det)
        nbStep2,rem2 = divmod(num2,det)
        if (nbStep1<0 or nbStep2<0 or rem1 != 0 or rem2 != 0):
            return 0 # 0 means impossible (or negative moves)
        return nbStep1 * 3 + nbStep2

lines = aoc.ReadPuzzleInput("input_day13.txt")
sections = aoc.ToSections(lines)
machines = [Machine([[(int(a),int(b)) for a,b in re.findall(".*:.*X.(\d*),.Y.(\d*)",line)]  for line in section]) for section in sections]

def part1():
    tokens = [m.tokenCost() for m in machines]
    print(sum(tokens))
    return 

def part2():
    tokens = [m.tokenCost(10000000000000) for m in machines]
    print(sum(tokens))  
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

