#Advent of code 2020: Day 23   
#https://adventofcode.com/2020/day/23
import re,sys,copy
import math,time,itertools
from functools import reduce

input = "789465123"
#input = "389125467"


deck = [int(x) for x in input]
maxNum = max(deck)

def playRound(deck : list):
    current = deck[0]
    pickUp = [deck.pop(1),deck.pop(1),deck.pop(1)]
    dest = current -1 
    if dest <1:
        dest = maxNum
    while dest in pickUp:
         dest = dest -1
         if dest <1:
             dest = maxNum
    destIndex = deck.index(dest) + 1
    deck[destIndex:destIndex] = pickUp 
    deck.append(deck.pop(0))
    

    return deck


def part1():
    global deck
    for i in range(100):
        deck = playRound(deck)

    text = "".join([str(x) for x in deck])
    print(text)

    return 

def part2():
    global deck
    deck = [int(x) for x in input]
    deck.extend(range(maxNum+1,1000001))

    for i in range(10000000):
        if i % 10000 == 0:
            print(i)
        deck = playRound(deck)

    ind = deck.index(1)
    v1 = deck[(ind+1)]
    v2 = deck[(ind+2)]
    print(ind, v1, v2, v1*v2)
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

