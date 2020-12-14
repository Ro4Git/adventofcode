#Advent of code 2020: Day 4
#https://adventofcode.com/2020/day/4
import re, time, copy

# eyr:2027
# hcl:#602927
# hgt:186cm byr:1939 iyr:2019 pid:552194973 ecl:hzl

f = open('input_day4.txt','r')
lines = f.readlines()
f.close()

requiredFields = ["byr","iyr","eyr","hgt","hcl","ecl","pid"]
validEyeColor = ["amb","blu","brn","gry","grn","hzl","oth"]

def validateDate(value, min, max):
    intval = int(value)
    return min <= intval <= max

def validateHeight(value):
    m = re.search('(.+?)(in|cm)', value)
    if m != None and len(m.groups()) == 2:
        height = int(m.groups()[0])
        if m.groups()[1] == "cm" and 150 <= height <= 193:
            return True
        if m.groups()[1] == "in" and 59 <= height <= 76:
            return True
    return False

def validateHair(value):
    m = re.search('#[a-f0-9_]{6}', value)
    return (m != None) 

def validatePID(value):
    m = re.search('[0-9]{9}', value)
    return (m != None) and len(value)==9
 
def printprob(problem,key):
#    print("----- ",key," ---" , problem[key])
    return

def validatePassportPart1(passport):
    if not all (k in passport.keys() for k in requiredFields):
        return False
    return True

def validatePassportPart2(passport):
    if not all (k in passport.keys() for k in requiredFields):
        return False
    if (not validateDate(passport["byr"],1920,2002)): 
        printprob(passport,"byr")
        return False
    if (not validateDate(passport["iyr"],2010,2020)): 
        printprob(passport,"iyr")
        return False
    if (not validateDate(passport["eyr"],2020,2030)): 
        printprob(passport,"eyr")
        return False        
    if (not validateHeight(passport["hgt"])): 
        printprob(passport,"hgt")
        return False    
    if (not validateHair(passport["hcl"])):
        printprob(passport,"hcl")
        return False
    if not passport["ecl"] in validEyeColor:
        printprob(passport,"ecl")
        return False
    if (not validatePID(passport["pid"])):
        printprob(passport,"pid")
        return False

    #print(passport)
    return True   

def part(validateFunc):
    validpassports = []
    passportData= {}
    for line in lines:
        tokens = line.split(" ")
        if tokens[0] != "\n" and tokens[0]!="":
            for token in tokens:
                key,value = token.split(":")
                passportData[key] = value.rstrip()
        else:
            #end ofsequence
            if validateFunc(passportData):
                validpassports.append(passportData.copy())
            passportData.clear()
    print(len(validpassports))


print("----- Part1 ----")
startp1 = time.time()
part(validatePassportPart1)
endp1 = time.time()
print("{:.4f}s".format(endp1 - startp1))

print("----- Part2 ----")
startp2 = time.time()
part(validatePassportPart2)
endp2 = time.time()
print("{:.4f}s".format(endp2 - startp2))

