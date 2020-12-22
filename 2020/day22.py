#Advent of code 2020: Day 22   
#https://adventofcode.com/2020/day/22
import re,sys,copy
import math,time,itertools
from functools import reduce

f = open('input_day22.txt', 'r')
lines = f.readlines()
f.close()

separator = lines.index("\n")
player1 = [int(x) for x in lines[1:separator]]
player2 = [int(x) for x in lines[separator+2:]]
print(player1)
print(player2)

def playRoundPart1():
    card1 = player1.pop(0)
    card2 = player2.pop(0)
    if card1 > card2: 
        player1.append(card1)
        player1.append(card2)
    else: 
        player2.append(card2)
        player2.append(card1)
    return

def winningScore(player):
    score = 0
    for i,a in enumerate(player):
        score = score + (len(player)-i)*a
    return score

verbose = False

def playGameRound2(subdeck1,subdeck2,gameIndex):
    rounds = []
    roundIndex =1
    if (verbose):
        print("==== Game ",gameIndex," ====")
        print("\n")

    def playRoundPart2():
        score1,score2 = winningScore(subdeck1),winningScore(subdeck2)
        if score1 == 0:
            return 2
        if score2 == 0:
            return 1            
        if (score1,score2) in rounds:
            #player1 won
            return -1
        rounds.append((score1,score2))
        card1 = subdeck1.pop(0)
        card2 = subdeck2.pop(0)
        winner = 0
        if (verbose):
            print("--- Round ",roundIndex , "(Game ",gameIndex,") ---")
            print("Player 1:",subdeck1)
            print("Player 2:",subdeck2)
            print("Player 1 card:",card1)
            print("Player 2 card:",card2)
        
        if (card1 <= len(subdeck1) and  card2 <= len(subdeck2)):
            deck1 = [x for x in subdeck1[0:card1]]
            deck2 = [x for x in subdeck2[0:card2]]
            if (verbose):
                print("Playing a sub-game to determine the winner...")
            winner = playGameRound2(deck1,deck2,gameIndex+1)
        else:
            if card1 > card2: 
                winner = 1
            else: 
                winner = 2
        if winner == 1: 
            subdeck1.append(card1)
            subdeck1.append(card2)
        else: 
            subdeck2.append(card2)
            subdeck2.append(card1)
        if (verbose):
            print("Winner of round ",roundIndex," of game", gameIndex, "=", winner)
        return winner       

    winner = 0
    while (len(subdeck1) and len(subdeck2)): 
        winner = playRoundPart2()
        if winner == -1:
            return 1
        roundIndex += 1
        

    return winner

def part1():
    while (len(player1) and len(player2)): 
        playRoundPart1()

    if len(player1):
        print("Player1",winningScore(player1))
    else:
        print("Player2",winningScore(player2))

    return 

def part2():
    global player1
    global player2
    player1 = [int(x) for x in lines[1:separator]]
    player2 = [int(x) for x in lines[separator+2:]]

    winner = playGameRound2(player1,player2,1)
    if len(player1):
        print("Player1",winningScore(player1))
    else:
        print("Player2",winningScore(player2))

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

