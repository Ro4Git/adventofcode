#Advent of code 2021: Day 8
#https://adventofcode.com/2021/day/8
import re, time, copy
from collections import defaultdict

f = open('input_day8.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

#dcga cadgbfe gecba cbfde eda cdbea gbadfe fegcba bedgca da | bgefdac bdace ad agcd

#  0:      1:      2:      3:      4:
# aaaa    ....    aaaa    aaaa    ....
#b    c  .    c  .    c  .    c  b    c
#b    c  .    c  .    c  .    c  b    c
# ....    ....    dddd    dddd    dddd
#e    f  .    f  e    .  .    f  .    f
#e    f  .    f  e    .  .    f  .    f
# gggg    ....    gggg    gggg    ....

#  5:      6:      7:      8:      9:
# aaaa    aaaa    aaaa    aaaa    aaaa
#b    .  b    .  .    c  b    c  b    c
#b    .  b    .  .    c  b    c  b    c
# dddd    dddd    ....    dddd    dddd
#.    f  e    f  .    f  e    f  .    f
#.    f  e    f  .    f  e    f  .    f
# gggg    gggg    ....    gggg    gggg

#1 = 2 = __c__f_ 
#4 = 4 = _bcd_f_
#7 = 3 - a_c__f_
#8 = 7 = abcdefg

#2 = 5 = a_cde_g
#3 = 5 = a_cd_fg
#5 = 5 = ab_d_fg - 

#6 = 6 = ab_defg -
#9 = 6 = abcd_fg - 
#0 = 6 = abc_efg -

groups = [line.split(' | ') for line in lines]
lefts = [line[0].split() for line in groups]
rights = [line[1].split() for line in groups]

def decodeLine(left):
    codes = [""]*10
    mapping = {}
    bylength = defaultdict(list)
    for l in left:
        bylength[len(l)].append(l)

    codes[1] = set(bylength[2][0])
    codes[4] = set(bylength[4][0])
    codes[7] = set(bylength[3][0])
    codes[8] = set(bylength[7][0])

    # 'a' is in 7 but not 1 
    mapping["a"] = (codes[1] ^ codes[7])
    # 'c' 6 is the only 6 length code  that doesn't ccontain "c"
    for s in bylength[6]:
        inter = (codes[1] & set(s))
        if len(inter) == 1:
            codes[6] = set(s)
            bylength[6].remove(s)
            break
    # 5
    for s in bylength[5]:
        inter = (codes[6] ^ set(s))
        if len(inter) == 1:
            codes[5] = set(s)
            bylength[5].remove(s)
            break
    #9 
    for s in bylength[6]:
       if ((codes[1] | codes[5]) == set(s)):
            codes[9] = set(s)
            bylength[6].remove(s)
            break
    codes[0] = set(bylength[6][0])
    # 3
    for s in bylength[5]:
        inter = (codes[1] & set(s))
        if len(inter) == 2:
            codes[3] = set(s)
            bylength[5].remove(s)
            break
    codes[2] = set(bylength[5][0])
    return codes

def part1():
    sel = [2,3,4,7]
    subset= [[num for num in r if len(num) in sel]  for r in rights]
    count = sum([len(n) for n in subset])
    print(count)
    return 

def part2():
    sum = 0
    for i,digits in enumerate(lefts):
        display = ""
        codes = decodeLine(digits)
        for s in rights[i]:
            for digit,c in enumerate(codes):
                if set(s) == c:
                    display += str(digit)
                    break
        print(display)
        sum += int(display)
    print("result:")
    print(sum)
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