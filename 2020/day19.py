#Advent of code 2020: Day 19
#https://adventofcode.com/2020/day/19
import regex,sys
import time,itertools
from functools import reduce

f = open('input_day19.txt', 'r')
lines = f.readlines()
f.close()

nbrules = lines.index("\n")
rules = [[]]*max(nbrules,1000)
expanded_rules = [""]*max(nbrules,1000)
tovalidate = []
for rule in lines[0:nbrules]:
    tokens = rule.split(": ")
    rules[int(tokens[0])] = [a.split() for a in tokens[1].rstrip().split("|")]
for line in lines[nbrules+1:]:
    tovalidate.append(line)

def expandSingle(rule,part2):
    if (len(rule) == 1):
        if rule[0][0] == '\"':
            return rule[0][1]
        else:
            return expandRule(int(rule[0]),part2)
    else:
        str1 = expandRule(int(rule[0]),part2)
        str2 = expandRule(int(rule[1]),part2)
        return str1 + str2
    return ""

def expandRule(index,part2):
    if (expanded_rules[index] != ""):
        return expanded_rules[index]
    rule = rules[index]
    matchStr = ""
    if len(rule) == 2:
        str1 = expandSingle(rule[0],part2)
        str2 = expandSingle(rule[1],part2)
        matchStr = '('  + str1 + "|" + str2  + ")"
    else:
        if part2 == True:
            if (index == 8):
                matchStr = "(" + expandSingle(rule[0],part2) + ")+"  
            elif index == 11:
                str1 = expandRule(int(rule[0][0]),part2)
                str2 = expandRule(int(rule[0][1]),part2)    
                matchStr = "((?P<g0>(?&g42)" + str2 + ")\\n" 
                # harcoded 4 because result does not change with higher combinations
                for i in range(4): 
                   matchStr += "|(?P<g" + str(i+1) + ">(?&g42)(?&g" + str(i) + ")(?&g31))\\n"                               
                matchStr += ")" 
            else:
                matchStr = expandSingle(rule[0],part2)
        else:
            matchStr = expandSingle(rule[0],part2)

    # will reuse these
    if (index == 42 or index == 31):
        matchStr = "(?P<g" + str(index) + ">" + matchStr + ")"
    
    expanded_rules[index] = matchStr

    #print(index, ": " , matchStr)
    return matchStr
    

def part(part2 : bool):
    global expanded_rules
    expanded_rules = [""]*max(nbrules,1000)
    expression = expandRule(0,part2)
    if (not part2):
        expression += "\\n"
    print(expression)

    nbMatch = 0
    for str in tovalidate:
        m = regex.match(expression,str)
        if (m != None):
            nbMatch += 1
    print(nbMatch)



print("----- Part1 ----")
startp1 = time.time()
part(False)
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part(True)
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))

