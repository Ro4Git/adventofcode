#Advent of code 2021: Day 16
#https://adventofcode.com/2021/day/16
import re, time, copy, math, sys


f = open('input_day16.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

hexadecimal = lines[0]
hexadecimal = "D2FE28"
binary = "".join([bin(int(c,16))[2:].zfill(4) for c in hexadecimal])
print(binary)

def decodePacket(code):
    l = 6
    version = int(code[0:3],2)
    type    = int(code[3:6],2)
    index = 6
    if type == 4:
        value = ""
        lv = code[index:index+5]
        while lv[0] != '0':
            value += lv[1:5] 
            index += 5  
            lv = code[index:index+5]
        value += lv[1:5] 
        index += 5  
        literal_value = int(value,2)
        index = (index+3) & ~3      
        print(f"lit value ({version},{type},{literal_value})")
    else:
        ltypeId = code[6]
        if ltypeId == '1':
            #nbsub packets = next 11
        else:
            #length = next 15
            


        return 

def part1():
    decodePacket(binary)
    return

def part2():
    return


print("----- Part1 ----")
startp1 = time.time()
displayPath  = part1()
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part2()
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))

