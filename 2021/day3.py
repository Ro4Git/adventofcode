#Advent of code 2021: Day 3
#https://adventofcode.com/2021/day/3
import re, time, copy

f = open('input_day3.txt','r')
lines = f.readlines()
f.close()

# B  01000010
# R  01010010
# F  01000110
# L  01001100

lines = [line.rstrip("\n") for line in lines]

nbbits = len(lines[0])
nbones=[0]*nbbits
nbnumbers = len(lines)

print(nbbits)
print(nbnumbers)

for line in lines:
    for i,c in enumerate(line):
        nbones[i] += int(c)

print(nbones)

def part1():
    mostcommon = ""
    leastcommon = ""
    for nbone in nbones:
        # more 1s than 0s ?
        if nbone*2 >= nbnumbers:
            mostcommon += '1'
            leastcommon += '0'
        else:
            mostcommon += '0'
            leastcommon += '1'

    print(mostcommon)
    print(leastcommon)
    gamma = int(mostcommon,2)
    epsilon = int(leastcommon,2)
    print(gamma*epsilon)

def filterlist_mostcommon(list,index):
    if (len(list) == 1):
        return list
    one_count = 0
    mostcommon = 1
    for line in list:
        one_count += int(line[index])
    if one_count*2 >= len(list):
        mostcommon = '1'
    else:
        mostcommon = '0'
    return [line for line in list if line[index] == mostcommon]

def filterlist_leastcommon(list,index):
    if (len(list) == 1):
        return list
    one_count = 0
    leastcommon = 1
    for line in list:
        one_count += int(line[index])
    if one_count*2 < len(list):
        leastcommon = '1'
    else:
        leastcommon = '0'
    return [line for line in list if line[index] == leastcommon]

def part2():
    O2genrating_list = lines
    for i in range(nbbits):
        O2genrating_list = filterlist_mostcommon(O2genrating_list,i)

    CO2scrubber_rating = lines
    for i in range(nbbits):
        CO2scrubber_rating = filterlist_leastcommon(CO2scrubber_rating,i)

    gamma = int(O2genrating_list[0],2)
    print(gamma)
    epsilon = int(CO2scrubber_rating[0],2)
    print(epsilon)
    print(gamma*epsilon)



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

