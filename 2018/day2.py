

initial_numbers= []


f = open('input_day2.txt','r')
lines = f.readlines()
f.close()

total2 = 0
total3 = 0

def processId(idstr):
    global total2
    global total3
    chars = [0]*256
    for c in idstr:
        chars[ord(c)] =  chars[ord(c)] + 1
    has2 = False
    has3 = False
    for c in chars:
        if c == 2 and not has2:
            has2 = True
            total2 = total2 + 1
        if c == 3 and not has3:
            has3 = True
            total3 = total3 + 1

def compareString(string1,string2):
    result = ""
    for i,c in enumerate(string1):
        if (c == string2[i]):
            result = result + c
    return result

def part1():
    for line in lines:
        processId(line)
    print(total2, total3, total2*total3)

def part2():
    maxlength = 0
    bestmatch = ""
    for i,line in enumerate(lines):
        for j in range (i+1, len(lines)):
            common = compareString(line,lines[j])
            if len(common) > len(bestmatch):
                bestmatch = common
    print(i,bestmatch)        

part1()
part2()