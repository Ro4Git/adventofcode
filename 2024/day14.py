#Advent of code 2024: Day 14
#https://adventofcode.com/2024/day/14
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

width = 101
height = 103

display = aoc.Display(True, width, height,    4 , 1)

class Robot:
    def __init__(self, data):
        self.pos = [data[0],data[1]]
        self.vel = [data[2],data[3]]
        
    def advance(self, nbSteps):
        self.pos = aoc.addPos(self.pos,aoc.sclPos(nbSteps,self.vel))
        self.pos = (self.pos[0] % width, self.pos[1] % height)
        
    def __str__(self):        
        return str(self.__dict__)  

lines = aoc.ReadPuzzleInput("input_day14.txt")
           

def part1():
    robots = [Robot([int(n) for n in re.findall("p=(.*\d*),(.*\d*) v=(.*\d*),(.*\d*)",line)[0]]) for line in lines]
    quadCount = [0,0,0,0]
    for robot in robots:
        robot.advance(100)
        # 0-49 50 51-100
        if (robot.pos[0] != width//2 and robot.pos[1] != height//2):
            index = 1 if robot.pos[0] > (width//2) else 0
            index += 2 if robot.pos[1] > (height//2) else 0
            quadCount[index] += 1
    print(quadCount)
    print(quadCount[0]*quadCount[1]*quadCount[2]*quadCount[3])
    return 

def part2():
    robots = [Robot([int(n) for n in re.findall("p=(.*\d*),(.*\d*) v=(.*\d*),(.*\d*)",line)[0]]) for line in lines]
    quadCount = [0,0,0,0]
    # pattern reappears at 57 + n1 * 103 or 86 + n2 * 101
    # easter egg at intersection
    # try 
    delta = 57
    step = 0
    while True:
        quadCount = [0,0,0,0]
        for robot in robots:
            robot.advance(delta)
        step += delta
        print(step)


        display.clear()
        display.drawListPos([r.pos for r in robots ],(100,255,100))
        display.update()

        delta = 0
        while delta == 0:
            aoc.pygame.display.update()
            for event in aoc.pygame.event.get():
                if event.type == aoc.pygame.KEYDOWN:
                    if event.key == aoc.pygame.K_LEFT:
                        delta = -103
                    elif event.key == aoc.pygame.K_RIGHT:
                        delta = 103
    
                    
    
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

display.wait()