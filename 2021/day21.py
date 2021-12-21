#Advent of code 2021: Day 21
#https://adventofcode.com/2021/day/21
import re, time, copy, sys, math, pygame
from collections import defaultdict
from itertools import combinations, combinations_with_replacement

from pygame.constants import CONTROLLER_BUTTON_RIGHTSHOULDER

f = open('input_day21.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

# display Data
screenSize = 1300
cellSize = 3
#cx= screenSize//2 - width*cellSize//2
#cy= screenSize//2 - height*cellSize//2


playerStartPos = [7,5]
playerPos = copy.copy(playerStartPos)
playerScore = [0,0]
currentDie = 1
nbRolls = 0

def dieRoll():
    global currentDie, nbRolls
    currentDie += 1
    nbRolls += 1
    if currentDie>100:
        currentDie = 1
    return currentDie-1

def rollPlayersPart1():
    global playerScore,playerPos
    for i in range(2):
        roll = dieRoll() + dieRoll() + dieRoll()
        newPos = playerPos[i] + roll
        newPos = ((newPos-1) % 10)+1
        playerPos[i] = newPos
        playerScore[i] += newPos
        if (playerScore[i]>=1000):
            break

# all possible permutations of 1,2,3 added together
possibleRolls = [x+y+z for x in range(1,4) for y in range(1,4) for z in range(1,4)]
# playerScoreDict: for a given score (key) => dictionary of current positions (key) and number of occurences of player being at that position with that score
playerScoreDict = [defaultdict(lambda: defaultdict(int)),defaultdict(lambda: defaultdict(int))]
playerScoreDict[0] = {0:{playerStartPos[0]:1}}
playerScoreDict[1] = {0:{playerStartPos[1]:1}}
winningUniverses = [0,0]

def rollPlayersPart2():
    global winningUniverses
    newScores = [defaultdict(lambda: defaultdict(int)),defaultdict(lambda: defaultdict(int))]
    for i,scores in enumerate(playerScoreDict):         # for all players
        for score,possPositions in scores.items():      # for each possible score at that step
            for pos in possPositions.keys():            # for each possible positions for this score
                for p1 in possibleRolls:                # for each possible die roll 
                    newPos = ((pos + p1 -1) % 10)+1
                    newScore = score + newPos           
                    if (newScore>=21):                  # winning roll: count how many possible universe in other player
                        nbWinning =  possPositions[pos]  # number of time this player is above 21
                        if i==0:
                            winningUniverses[i] += nbWinning * sum([sum(otherPos.values()) for otherPos in playerScoreDict[1].values()]) # number of time player 1 is below 21
                        else:
                            winningUniverses[i] += nbWinning * sum([sum(otherPos.values()) for otherPos in newScores[0].values()]) # number of time player 0 is below 21
                    else:
                        newScores[i][newScore][newPos] = newScores[i][newScore][newPos] + possPositions[pos]
    return newScores


def part1():
    while(playerScore[0]<1000 and playerScore[1]<1000):
        rollPlayersPart1()
    print(nbRolls * min(playerScore))
    return

def part2():
    global playerScoreDict
    while len(playerScoreDict[0].items())>0 and len(playerScoreDict[1].items())>0:
        playerScoreDict = rollPlayersPart2()
    print(winningUniverses)
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

