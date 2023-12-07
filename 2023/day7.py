#Advent of code 2023: Day 7
#https://adventofcode.com/2023/day/7
import re, time, copy, math

f = open('input_day7.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

hands = [(line.split()[0],int(line.split()[1])) for line in lines ]

cards = {'A':0xe,'K':0xd,'Q':0xc,'J':0xb,'T':0xa,'9':9,'8':8,'7':7,'6':6,'5':5,'4':4,'3':3,'2':2}
cards_p2 = {'A':0xe,'K':0xd,'Q':0xc,'J':1,'T':0xa,'9':9,'8':8,'7':7,'6':6,'5':5,'4':4,'3':3,'2':2}

def valueFct(hand): 
    # 5 of a kind
    # 4 of a kind
    # full 
    # 3 of a kind
    # 2 pairs
    # pair
    # card
    nbs = [0]*13 
    for i,card in enumerate(cards.keys()):
        nbs[i] = hand.count(card)
 
    subSort = 0
    if 5 in nbs:
        subSort = 0xf
    elif 4 in nbs:
        subSort = 0xe
    elif 3 in nbs:
        if 2 in nbs:
            subSort = 0xd
        else:
             subSort = 0xc
    else:
        nb2 = nbs.count(2)
        subSort = nb2

    for i in range(5):       
        subSort = (subSort << 4) + cards[hand[i]]
    return subSort


def part1():
    sortedHands = sorted(hands,key=lambda x:valueFct(x[0]))

    res = 0
    for i,s in enumerate(sortedHands):
        res = res + (i+1)*s[1]

    print(res)
    return 


def valueFct_p2(hand): 
    # 5 of a kind
    # 4 of a kind
    # full 
    # 3 of a kind
    # 2 pairs
    # pair
    # card
    nbs = [0]*13 
    nbJ = 0
    for i,card in enumerate(cards.keys()):
        if card != 'J':
            nbs[i] = hand.count(card)
        else:
            nbJ = hand.count(card)

    subSort = 0
    if 5 in nbs or (5-nbJ) in nbs:
        subSort = 0xf
    elif 4 in nbs or (4-nbJ) in nbs:
        subSort = 0xe
    elif 3 in nbs:
        if 2 in nbs:
            subSort = 0xd
        else:
             subSort = 0xc
    elif nbJ==1 and 2 in nbs:
        if nbs.count(2) ==2:
            subSort = 0xd
        else:
            subSort = 0xc
    elif nbJ==2:         
        subSort = 0xc
    else:
        nb2 = nbs.count(2) #- cannot have 2 J at this stage or even 1 J and 1 pair
        if nb2 == 2:
            subSort = 2
        elif nb2 ==1 or nbJ == 1:
            subSort = 1

    for i in range(5):       
        subSort = (subSort << 4) + cards_p2[hand[i]]
    return subSort


def part2():

    sortedHands = sorted(hands,key=lambda x:valueFct_p2(x[0]))
    res = 0
    for i,s in enumerate(sortedHands):
        res = res + (i+1)*s[1]
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