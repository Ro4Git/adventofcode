#Advent of code 2020: Day 25
#https://adventofcode.com/2020/day/25
import re,sys,copy
import math,time,itertools
from functools import reduce

f = open('input_day25.txt', 'r')
lines = f.readlines()
f.close()

cardPublicKey = 14205034
doorPublicKey = 18047856

def modinv(a, m):
    return pow(int(a), int(m-2), int(m))

def transform(subject,loopSize):
    d = pow(subject, loopSize, 20201227) 
    return d



def part1():
    loopSizeCard = 0
    res = 0
    while res != cardPublicKey:
        loopSizeCard += 1
        res = transform(7, loopSizeCard)
        
    print("loop size card:",loopSizeCard)
    encryptionKey = transform(doorPublicKey,loopSizeCard)
    print("encryptionKey:",encryptionKey)
    
    return 

def part2():

    test = transform(7,8)
    print(test)
    
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

