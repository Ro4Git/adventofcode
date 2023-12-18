#Advent of code 2023: Day 15
#https://adventofcode.com/2023/day/15
import re, time, copy, math
from functools import cache

f = open('input_day15.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

seqs = lines[0].split(',')
print(seqs)

def hashSeq(seq):
    code = 0 
    for c in seq: 
        code += ord(c)
        code *= 17
        code = code & 255
    return code
codes = [hashSeq(seq) for seq in seqs]

boxes = []

for i in range(256):
    boxes.append([])

def sortBoxes():
    global boxes
    for i,seq in enumerate(seqs): 
        if seq[-1] == '-': 
            label = seq[:-1]
            hash = hashSeq(label)
            boxes[hash] = [box for box in boxes[hash] if box[0:len(label)] != label]
        else: 
            str = seq
            label = seq[:-2]
            hash = hashSeq(label)
            str = str.replace("="," ")
            for i,b in enumerate(boxes[hash]):
                if b[0:len(label)] == label:
                    boxes[hash][i] = str
                    break
            else:
                boxes[hash].append(str)


def part1():
    print(sum(codes))
    return 

def part2():
    sortBoxes()
    print(codes)
    print(boxes)

    focusingPower = 0
    for i,b in enumerate(boxes):
        for j,lens in enumerate(b):
            focusingPower += (1 + i) * (1+j) * int(lens[-1])
    print(focusingPower)

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