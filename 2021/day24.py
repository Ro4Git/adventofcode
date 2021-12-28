#Advent of code 2021: Day 24
#https://adventofcode.com/2021/day/24
import re, time, copy, sys, math

f = open('input_day24.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

#inp w
#mul x 0
#add x z
#mod x 26
#div z 1
#add x 10   => Line 5 num1
#eql x w
#eql x 0
#mul y 0
#add y 25
#mul y x
#add y 1
#mul z y
#mul y 0
#add y w
#add y 13  => Line 16 num 2
#mul y x
#add z y

nums = [(int(lines[i * 18 + 5][6:]), int(lines[i * 18 + 15][6:])) for i in range(14)]
propagate = []
chains = {}
for i, num in enumerate(nums):
    if num[0] > 0:
        propagate.append((i, num[1]))
    else:
        prev = propagate.pop()
        chains[i] = (prev[0], prev[1] + num[0])


def part1():
    numbers = {}
    for i, chain in chains.items():
        numbers[i] = min(9, 9 + chain[1])
        numbers[chain[0]] = min(9, 9 - chain[1])
    print("".join(str(numbers[x]) for x in range(14)))
    return

def part2():
    numbers = {}
    for i, chain in chains.items():
        numbers[i] = max(1, 1 + chain[1])
        numbers[chain[0]] = max(1, 1 - chain[1])
    print("".join(str(numbers[x]) for x in range(14)))
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

