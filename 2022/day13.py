#Advent of code 2022: Day 13
#https://adventofcode.com/2022/day/13
import re, time, copy, functools
import ast

f = open('input_day13.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

pairs=[]
for i in range(len(lines)//3):
    pairs.append([ast.literal_eval(lines[i*3]),ast.literal_eval(lines[i*3+1])])

listPackets = [ast.literal_eval(line) for line in lines if len(line)>0]

def compare(list1,list2):
    t1 = type(list1)
    t2 = type(list2)
    if t1 == t2:
        if t1 == int:
            return list2-list1
        if t1 == list:
            maxLength = max(len(list1),len(list2))
            for i in range(maxLength):
                if i>=len(list2):
                    return -1
                if i>=len(list1):
                    return 1                    
                res = compare(list1[i],list2[i])
                if res!=0:
                    return res
        return 0
    else: #T1 != T2
        if t1 == int:
            return compare([list1],list2)
        else:
            return compare(list1,[list2])
    

def part1():
    incorrects = []
    for index,p in enumerate(pairs):
        res = compare(p[0],p[1])
        if (res>0):
            incorrects.append(index+1)
    print(incorrects)
    print(sum(incorrects))
    return


def part2():
    listPackets.append([[2]])
    listPackets.append([[6]])
    sortedPackets = sorted(listPackets, key=functools.cmp_to_key(compare),reverse=True)
    index1 = 0
    index2 = 0
    for i,packet in enumerate(sortedPackets):
        rep = str(packet)
        if rep == "[[2]]":
            index1 = i+1
        if rep == "[[6]]":
            index2 = i+1
    print(sortedPackets)
    print(index1,index2)
    print(index1*index2)
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