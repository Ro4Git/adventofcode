#Advent of code 2020: Day 12
#https://adventofcode.com/2020/day/12
import sys,pygame,time


f = open('input_day12.txt', 'r')
lines = f.readlines()
f.close()

ddirs = {"E":0,"S":1,"W":2,"N":3}
dirs = [(1,0),(0,-1),(-1,0),(0,1)]

def rescale(v,w,r):
    return ((v[0]-w[0])*r, (v[1]-w[1])*r)

def add(v,w):
    return (v[0]+w[0], v[1]+w[1])

def advance(pos, delta, mul):
    return (pos[0] + delta[0]*mul,pos[1] + delta[1]*mul)

def rotateccw(cpos, pos, steps):
    npos = (pos[0] - cpos[0], pos[1] - cpos[1])
    for i in range(steps):
        npos = (-npos[1],npos[0])
    return (npos[0] + cpos[0], npos[1] + cpos[1])

def rotatecw(cpos, pos, steps):
    npos = (pos[0] - cpos[0], pos[1] - cpos[1])
    for i in range(steps):
        npos = (npos[1],-npos[0])
    return (npos[0] + cpos[0], npos[1] + cpos[1])


def display(positions):
    minp = (0,0)
    maxp = (0,0)    
    for p in position:    
        minp = (min(minp[0],pos[0]),min(minp[1],pos[1]))            
        maxp = (max(maxp[0],pos[0]),max(maxp[1],pos[1]))
    pygame.init()
    width, height = maxp[0]-minp[0], maxp[1]-minp[1]
    ratio = 512 / max(width, height)
    screen = pygame.display.set_mode((512,512))   
    prevp = positions[0]
    screen.fill((255,255,255,255))
    for p in positions:
        pygame.draw.line(screen,(0, 0, 0, 0),rescale(prevp,minp,ratio),rescale(p,minp,ratio),3)
        prevp = p
    pygame.display.flip()     
    input("Press Enter to continue...")       
    return


def part1():
    positions = []
    currentdir = int(0)
    pos = (0,0)
    for line in lines:
        command = line[0]
        val = int(line[1:])
        if (command=="R"):
            val = int(val/90)
            currentdir = (currentdir + val) & 3
        elif (command=="L"):
            val = int(val/90)
            currentdir = (currentdir + 4 - val) & 3
        elif (command=="F"):
            pos = advance(pos,dirs[currentdir],val)
        else:
            pos = advance(pos,dirs[ddirs[command]],val)
        positions.append(pos)
    #display(positions)
    print("part1:",pos, abs(pos[0]) + abs(pos[1]))

def part2():
    currentdir = int(0)
    wpos = (10,1)
    pos = (0,0)
    positions = []
    for line in lines:
        command = line[0]
        val = int(line[1:])
        if (command=="R"):
            val = int(val/90)
            wpos = rotatecw(pos, wpos,val)
        elif (command=="L"):
            val = int(val/90)
            wpos = rotateccw(pos, wpos,val)
        elif (command=="F"):
            delta = (wpos[0]- pos[0] , wpos[1]- pos[1])
            pos = advance(pos,delta,val)
            wpos = advance(wpos,delta,val)
        else:
            wpos = advance(wpos,dirs[ddirs[command]],val)
        positions.append(pos)
    #display(positions)
    print("part2:",pos , wpos, abs(pos[0]) + abs(pos[1]))


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