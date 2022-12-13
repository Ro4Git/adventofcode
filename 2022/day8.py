#Advent of code 2022: Day 8
#https://adventofcode.com/2022/day/8
import re, time, copy

f = open('input_day8.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

grid = []
for line in lines:
    grid.append([int(c) for c in list(line)])
width = len(grid[0])
height = len(grid)

def gridPixel(pos):
    return grid[pos[1]][pos[0]]

def isVisible(pos):
    treeHeight = gridPixel(pos)
    sideHidden = 0
    for x in range(0,pos[0]):
        if grid[pos[1]][x] >= treeHeight: 
            sideHidden+=1
            break
    for x in range(pos[0]+1,width):
        if grid[pos[1]][x] >= treeHeight: 
            sideHidden+=1
            break
    for y in range(0,pos[1]):
        if grid[y][pos[0]] >= treeHeight: 
            sideHidden+=1
            break
    for y in range(pos[1]+1,height):
        if grid[y][pos[0]] >= treeHeight: 
            sideHidden+=1
            break
    return sideHidden < 4


def part1():
    nbVisible = width*2 +(height-2)*2
    for x in range(1,width-1):
        for y in range(1,height-1):
            nbVisible += isVisible((x,y))
    print(nbVisible)
    return 

def treeViewScore(pos):
    treeHeight = gridPixel(pos)
    viewScore = 1
    for x in range(pos[0]-1,-1,-1):
        score = (pos[0] - x)
        if grid[pos[1]][x] >= treeHeight: 
            break
    viewScore = viewScore * score
    for x in range(pos[0]+1,width):
        score = (x - pos[0])
        if grid[pos[1]][x] >= treeHeight: 
            break
    viewScore = viewScore * score
    for y in range(pos[1]-1,-1,-1):
        score = (pos[1] - y)
        if grid[y][pos[0]] >= treeHeight: 
            break
    viewScore = viewScore * score
    for y in range(pos[1]+1,height):
        score = (y - pos[1])
        if grid[y][pos[0]] >= treeHeight: 
            break
    viewScore = viewScore * score
    return viewScore

def part2():
    maxScore = 0
    for x in range(1,width-1):
        for y in range(1,height-1):
            score = treeViewScore((x,y))
            if (score > maxScore):
                maxScore = score
    print(maxScore)    
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