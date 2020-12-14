#Advent of code 2020: Day 9
#https://adventofcode.com/2020/day/9
import time,re

f = open('input_day9.txt','r')
lines = f.readlines()
f.close()

values = []
possible_sums = []

for line in lines:
    value = int(line)
    values.append(value)


def build_sums(window):
    for i,v in enumerate(window):
        possible_sums.append([])
        for j in range(i+1,len(window)):
            sum = window[i] + window[j]
            possible_sums[i].append(sum)

# try to add a number to the window
def checknumber(value,window):
    # check if in existing sums 
    valid = False
    for i in range(0,24):
        if value in possible_sums[i]:
            valid = True
            break
    if not valid:
         return value

    #insert new item 
    possible_sums.pop(0)
    possible_sums.append([])
    window25.pop(0)
    window25.append(value)
    for i in range(0,24):
        possible_sums[i].append( value + window25[i])
    return 0

window25 = values[0:25]
build_sums(window25)


def part1():
    for i in range(25,len(values)):
        res = checknumber(values[i],window25)
        if res != 0:
            print(res)
            break
    return 0

def part2():
    for i in range(0,len(values)):
        sum = values[i]
        minv =  maxv = values[i]
        for j in range(i+1,len(values)):
            sum += values[j]
            minv = min(minv,values[j])
            maxv = max(maxv,values[j])
            if (sum >= 756008079):
                end = values[j]
                break
        if (sum == 756008079):
            print("Found : ",minv,maxv, minv+maxv)
    return 0

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