import copy 
import numpy
import pygame
import itertools



nbPassword = 0

def validPassword(password):
    prevdigit = 0
    nbrep = 0
    reps = []
    for j in range(0,6): 
        digit = int(password[j])
        if (digit<prevdigit):
            return False
        if (digit == prevdigit):
            nbrep = nbrep + 1
        else:
            reps.append(nbrep)
            nbrep = 0
        prevdigit = digit
    if (nbrep>0):
        reps.append(nbrep)
    return 1 in reps



for i in range(236491,713787):
    numb = str(i)
    if validPassword(numb):
        nbPassword = nbPassword + 1
        print(numb)

print("result")
print(nbPassword)




