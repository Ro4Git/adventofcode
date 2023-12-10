#Advent of code 2023: Day 9
#https://adventofcode.com/2023/day/9
import re, time, copy, math

f = open('input_day9.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()


sequences = [[int(n) for n in rng] for rng in [line.split(" ") for line in lines]]
print(sequences)

def deltas(input):
    return [c - input[i] for i,c in enumerate(input[1:])]

def getNextValue(input):
    seqs = []
    currentSeq = input.copy()
    seqs.append(currentSeq)
    while not all(d == 0 for d in currentSeq):
        currentSeq = deltas(currentSeq)
        seqs.append(currentSeq)
    seqs[-1][-1] = 0
    for i in reversed(range(0,len(seqs)-1)):
        seqs[i].append(seqs[i+1][-1] + seqs[i][-1])
    return seqs[0][-1]

def getPrevValue(input):
    seqs = []
    currentSeq = input
    seqs.append(currentSeq)
    while not all(d == 0 for d in currentSeq):
        currentSeq = deltas(currentSeq)
        seqs.append(currentSeq)
    seqs[-1][0] = 0
    for i in reversed(range(0,len(seqs)-1)):
        seqs[i][0] = seqs[i][0] - seqs[i+1][0]
    print(seqs)
    return seqs[0][0]



def part1():
    histories = [getNextValue(seq) for seq in sequences]
    print(sum(histories))
    return 

def part2():
    histories = [getPrevValue(seq) for seq in sequences]
    print(sum(histories))
 

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