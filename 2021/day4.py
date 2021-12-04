#Advent of code 2021: Day 4
#https://adventofcode.com/2021/day/4
import re, time, copy,numpy as np

f = open('input_day4.txt', 'r')
lines = f.readlines()
f.close()

class Board:
    def __init__(self,board):
        self.board = np.array(board,np.uint64)
        self.mark = np.ones((5,5),np.uint64)

    def __str__(self):
        output = "\n"
        for i in range(5):
            output += str(self.board[i]) + str(self.mark[i]) + "\n" 
        
        return output

    def __repr__(self):
        return str(self)

    def winBoard(self,num):
        print("winning board")
        print(self)
        print(num)
        sum = 0
        for i in range(5):
            for j in range(5):
                sum += self.board[i,j] * self.mark[i,j]
        print(sum * num)

    def markNumber(self,num):
        res = np.where(self.board == num)
        if res and res[0].size >0:
            self.mark[res[0][0], res[1][0]] = 0
            return self.checkWin()
        return False

    def checkWin(self):
        for r in self.mark:
            if not np.any(r):
                return True
        for c in self.mark.transpose():
            if not np.any(c):
                return True             
        return False

def readBoard(index):
    board = []
    for i in range(5):
        board.append( [ int(n) for n in lines[index+i].split()])
    return board
    
numbers = [int(c) for c in lines[0].split(',')]

index = 2
boards = []
while index<len(lines):
    boards.append(Board(readBoard(index)))
    index += 6


def part1():
    # first board to win
    finished = False
    for num in numbers:
        for board in boards:
            if board.markNumber(num):
                board.winBoard(num)
                finished = True
                break
        if finished:
            break
    return 

def part2():
    #last board to win
    lboards = boards
    for num in numbers:
        # remove all winning boards until there is only one left
        if len(lboards)>1:
            lboards = [board for board in lboards if not board.markNumber(num)]
        else:
            if lboards[0].markNumber(num):
                lboards[0].winBoard(num)
                break
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