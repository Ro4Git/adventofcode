#Advent of code 2020: Day 21   
#https://adventofcode.com/2020/day/21
import re,sys,copy
import math,time,itertools
from functools import reduce

f = open('input_day21.txt', 'r')
lines = f.readlines()
f.close()

liste = []
dictA = {}
dictI = {}
for l in lines: 
    m = re.match("(.+) \((.+)\)",l)
    ingredients = m.groups()[0].split(" ")
    allergens = m.groups()[1].replace("contains ","").split(", ")
    liste.append((ingredients,allergens))
    for a in allergens:
        dictA[a] = 1
    for i in ingredients:
        dictI[i] = 1

listI = [k for k in dictI.keys()]
listA = [k for k in dictA.keys()]

#interesct all lines containiing this allergen to only keep the common ingredients
potentials = {}
for a in listA:
    potentials[a] = [k for k in dictI.keys()]
    for ingredients,allergens in liste:
        if (a in allergens):
            potentials[a] = [i for i in potentials[a] if i in ingredients]

#recursively remove ingrdients that can only be assigned one allergen
finals = {}
while len(potentials) != len(finals):
    for k,v in potentials.items():
        if len(v) == 1 and not k in finals:
            finals[k] = v[0]
            for k1,v1 in potentials.items():
                if (k1 != k): 
                    try:
                        v1.remove(v[0])
                    except:
                        continue
            break
print(finals)
notSafeIngredients = {v:k for k,v in finals.items()}

def part1():
    nbSafe = 0
    for ingredients,allergens in liste:
        for ing in ingredients:
            if (not ing in notSafeIngredients):
                nbSafe += 1    
    print(nbSafe)
    return 

def part2():
    global listA
    listA.sort()
    canondang = [finals[a] for a in listA]
    res = ",".join(canondang)
    print(res)

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

