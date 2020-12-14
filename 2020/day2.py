#Advent of code 2020: Day 2
#https://adventofcode.com/2020/day/2
import re, time, copy


f = open('input_day2.txt','r')
lines = f.readlines()
f.close()

def processPolicy(idstr):
    #4-8 g: ggtxgtgbg
    tokens = re.split('-| |: |\n',idstr)
    minc = int(tokens[0])
    maxc = int(tokens[1])
    cchar = tokens[2]
    ccount = tokens[3].count(cchar)
    if (ccount>=minc and ccount <=maxc):
        return tokens[3]
    return ""

def processPolicy2(idstr):
    #4-8 g: ggtxgtgbg
    tokens = re.split('-| |: |\n',idstr)
    minc = int(tokens[0])
    maxc = int(tokens[1])
    cchar = tokens[2]
    if (tokens[3][minc-1] == cchar) ^ (tokens[3][maxc-1] == cchar):
        return tokens[3]
    return ""


def part(func):
    validlist = []
    for line in lines:
        res = func(line)
        if res != "":
            validlist.append(res)
    print(len(validlist))


print("----- Part1 ----")
startp1 = time.time()
part(processPolicy)
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part(processPolicy2)
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))