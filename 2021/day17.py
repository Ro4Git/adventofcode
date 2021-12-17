#Advent of code 2021: Day 17
#https://adventofcode.com/2021/day/17
import re, time, copy, math, sys


f = open('input_day17.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

targetArea = ((20,-10),(30,-5))
targetArea = ((155,-117),(182,-67))
#target area: x=155..182, y=-117..-67

# sumxVelocity = n*(n+1)/2 (xVel)
# maxY = n*(n+1)/2 (yVel)
# maxDeltaY = targetArea[1][1] - targetArea[0][1] // velocity cannot be bigger than this or it will overshoot
def findXVelocityRange():
    minV = 0
    for i in range(targetArea[0][0]):
        vel = i+1
        finalXPos = (vel * (vel+1))//2
        if finalXPos < targetArea[0][0]:
            #will never reach target
            continue
        elif finalXPos > targetArea[1][0]:
            maxV = i
            #will likely overshoot, 
            break
        else:
            if minV == 0: 
                minV = i+1
    return (minV,maxV)



def part1():
    xVelRange = findXVelocityRange()
    print(xVelRange)

    maxHit = 0
    for t in range(9,200): 
        pos = (0,0)
        vel = (xVelRange[0],t)
        testMaxY = t*(t+1)//2 
        hasTouched = False        
        while pos[1] > targetArea[1][1]:
            pos = (pos[0] + vel[0], pos[1] + vel[1])
            if (vel[0]>0):
                vel = (vel[0] - 1, vel[1]-1)
            else:
                vel = (0, vel[1]-1)
            if pos[1] <= targetArea[1][1] and pos[1] >= targetArea[0][1] and pos[0] <= targetArea[1][0] and pos[0] >= targetArea[0][0]:
                maxHit = t
                hasTouched = False
                break
    print(maxHit)
    print(maxHit*(maxHit+1)//2)
    return

def part2():
    solutions = []
    maxHit = 0
    maxPos = (0,0)
    minPos = (0,0)
    for xvel in range(1,targetArea[1][0]+2): 
        for yvel in range(targetArea[0][1]-2,400): 
            pos = (0,0)
            vel = (xvel,yvel)
            hasTouched = False        
            while pos[1] >= targetArea[0][1]-1 and pos[0]<targetArea[1][0]+1:
                pos = (pos[0] + vel[0], pos[1] + vel[1])
                maxPos = (max(maxPos[0],pos[0]),max(maxPos[1],pos[1]))
                minPos = (min(minPos[0],pos[0]),min(minPos[1],pos[1]))
                if (vel[0]>0):
                    vel = (vel[0] - 1, vel[1]-1)
                else:
                    vel = (0, vel[1]-1)
                if pos[1] <= targetArea[1][1] and pos[1] >= targetArea[0][1] and pos[0] <= targetArea[1][0] and pos[0] >= targetArea[0][0]:
                    hasTouched = True
                    solutions.append((xvel,yvel))
                    break
    print(len(solutions))
    print(maxPos)
    print(minPos)


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

