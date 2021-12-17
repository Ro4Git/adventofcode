#Advent of code 2021: Day 16
#https://adventofcode.com/2021/day/16
import re, time, copy, math, sys
from functools import reduce 
import operator

f = open('input_day16.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

hexadecimal = lines[0]
#hexadecimal = "A0016C880162017C3686B18A3D4780"
binary = "".join([bin(int(c,16))[2:].zfill(4) for c in hexadecimal])
#print(binary)

def decodePacket(code,parent):
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
        parent.append((version,type,literal_value))
        return index
    else:
        ltypeId = code[6]
        index = 7
        if ltypeId == '1':
            #nbsub packets = next 11
            nbsubPackets = int(code[index:index+11],2)
            index += 11
            newparent = []
            for i in range(nbsubPackets):
                advance = decodePacket(code[index:],newparent)
                index += advance      
            parent.append((version,type,newparent))          
        else:
            #length = next 15
            # then subpackets
            length = int(code[index:index+15],2)
            index += 15
            endindex = index + length
            newparent = []
            while index < endindex:
                advance = decodePacket(code[index:],newparent)
                index += advance
            index = endindex
            parent.append((version,type,newparent))
    return index

def versionSum(listPacket):
    sum = 0
    for item in listPacket:
        version = item[0]
        sum += version
        if (type(item[2]) is list):
            sum += versionSum(item[2])
    return sum

def evalPacket(packet):
    type = packet[1]
    if (type == 0): 
        return sum([evalPacket(item) for item in packet[2]])
    elif (type == 1): 
        return reduce(operator.mul, [evalPacket(item) for item in packet[2]], 1)
    elif (type == 2): 
        return min([evalPacket(item) for item in packet[2]])
    elif (type == 3):
        return max([evalPacket(item) for item in packet[2]])
    elif (type == 4):
        return packet[2]
    elif (type == 5):
        return int(evalPacket(packet[2][0]) > evalPacket(packet[2][1]))
    elif (type == 6):
        return int(evalPacket(packet[2][0]) < evalPacket(packet[2][1]))
    elif (type == 7):
        return int(evalPacket(packet[2][0]) == evalPacket(packet[2][1]))
    return 0


def part1():
    packetList = []
    decodePacket(binary,packetList)
    sum = versionSum(packetList)
    print(sum)
    print(len(packetList))
    return

def part2():
    packetList = []
    decodePacket(binary,packetList)    
    res = evalPacket(packetList[0])
    print(res)
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

