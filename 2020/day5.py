#Advent of code 2020: Day 5
#https://adventofcode.com/2020/day/5
import re, time, copy

f = open('input_day5.txt','r')
lines = f.readlines()
f.close()

# B  01000010
# R  01010010
# F  01000110  
# L  01001100

max_id = 0
seats=[0]*1024
for line in lines:
    id = 0
    for i in range(0,10): 
        id = id | ((not (ord(line[i]) & 4)) << (9-i))
    seats[id] = 1
    max_id = max(id,max_id)

def part1():
    print(max_id)

def part2():
    for i in range(1,max_id):
        if (seats[i] == 0 and seats[i+1] == 1 and seats[i-1] == 1):
            print(i)


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

