#Advent of code 2024: Day 21
#https://adventofcode.com/2024/day/21
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day21.txt")

class BestPathHolder:
    def __init__(self,digits, toPos):
        self.bestPaths = {}
        voidPos = toPos["#"]
        # compute best path from one digit of the keypad to another
        for (d1, d2) in itertools.product((c for c in digits if c != '#'), repeat=2):
            key = (d1,d2)
            if d1 == d2:
                self.bestPaths[key] = ['']
            else:
                # positions of digit in keypad
                p1 = toPos[d1]
                p2 = toPos[d2]
                delta = aoc.subPos(p2,p1)
                # repeat hor + vert moves
                xMovs = ['<', '>'][delta[0] > 0] * abs(delta[0])
                yMovs = ['^', 'v'][delta[1] > 0] * abs(delta[1])
                if (xMovs == 0):
                    self.bestPaths[key] = [yMovs]
                elif (yMovs == 0):
                    self.bestPaths[key] = [xMovs]
                else:
                    # void is in corner, only allow path that avoid that corner
                    if voidPos == (p2[0],p1[1]):
                        self.bestPaths[key] = [yMovs + xMovs] # moving x first would hit the void
                    elif voidPos == (p1[0],p2[1]):
                        self.bestPaths[key] = [xMovs + yMovs] # moving y first would hit the void
                    else:
                        self.bestPaths[key] = [xMovs + yMovs, yMovs + xMovs]
    def get(self, key):
        return self.bestPaths[key]

#    +---+---+
#  # | ^ | A |
#+---+---+---+
#| < | v | > |
#+---+---+---+
dirs = "#^A<v>"
dirKeypad = ["#^A","<v>"]
gridDir = aoc.ToGrid(dirKeypad)
dirsToPos = {c:gridDir.Find(c) for c in dirs}
bestPathsDir = BestPathHolder(dirs,dirsToPos)

#+---+---+---+
#| 7 | 8 | 9 |
#+---+---+---+
#| 4 | 5 | 6 |
#+---+---+---+
#| 1 | 2 | 3 |
#+---+---+---+
#  # | 0 | A |
#    +---+---+
nums = "789456123#0A"
numKeypad = ["789","456","123","#0A"]
gridNum = aoc.ToGrid(numKeypad)
numsToPos = {c:gridNum.Find(c) for c in nums}
bestPathsNum = BestPathHolder(nums,numsToPos)



@functools.cache
def sequence(code , depth, bestPaths =  bestPathsNum):
  if depth <= 0:
    return code

  result = ""
  for fromTo in aoc.pairwise('A' + code):
    results = [sequence(path + 'A', depth - 1, bestPathsDir) for path in bestPaths.get(fromTo)]
    result += results[0]
  return result

@functools.cache
def lensequence(code , depth, bestPaths =  bestPathsNum):
  if depth <= 0:
    return len(code)
  result = 0
  for fromTo in aoc.pairwise('A' + code):
    result += min(lensequence(path + 'A', depth - 1, bestPathsDir) for path in bestPaths.get(fromTo))
  return result

def complexity_p1(code,depth):
    result = sequence(code,depth,bestPathsNum)
    value = int(code[:-1])
    print(code, ':' , len(result), value , result)
    return value * len(result)

def complexity_p2(code,depth):
    result = lensequence(code,depth,bestPathsNum)
    value = int(code[:-1])
    print(code, ':' , result, value)
    return value * result

def part1():
    comps = [complexity_p1(code,5) for code in lines]
    print(comps)
    print(sum(comps))
    return 

def part2():
    comps = [complexity_p2(code,26) for code in lines]
    print(comps)
    print(sum(comps))
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


        

nbRobot = 8
keypadWidth = 192
robotOffset = (140,245)
lengthArm1 = (30,30*128/192)
lengthArm2 = (70,70*128/192)
armStartPos = (30,30)

def shadeCircle(surface,pos,radius):
    color1 = (170,168,80)
    color2 = (210,195,102)
    color3 = (65,79,22)
    aoc.pygame.draw.circle(surface,color3,pos,radius)
    aoc.pygame.draw.circle(surface,color2,aoc.addPos(pos,(1,2)),radius-2)
    aoc.pygame.draw.circle(surface,color1,aoc.addPos(pos,(3,4)),radius-6)

def shadeLine(surface,pos1, pos2):
    color1 = (170,168,80)
    color2 = (210,195,102)
    color3 = (65,79,22)
    aoc.pygame.draw.line(surface,color3,pos1,pos2,width = 8)
    aoc.pygame.draw.line(surface,color2,pos1,pos2,width = 6)
    aoc.pygame.draw.line(surface,color1,pos1,pos2,width = 4)


class Robot:
    def __init__(self, spr, index, cToPos):
        self.spr = spr
        self.index = index
        self.cToPos = cToPos
        self.advance = (0,0)
        self.targetPos = cToPos['A']
        self.color1 = (170,168,80)
        self.color2 = (210,195,102)
        self.color3 = (65,79,22)
        self.pos = (index * keypadWidth+robotOffset[0], robotOffset[1])
        self.next = None
        
    def press(self):
        if self.next != None:
            if self.cToPos == dirsToPos:
                c = gridDir.Val(self.targetPos)
            else:
                c = gridNum.Val(self.targetPos)     
            self.next.move(c)
      
    def move(self,c):
        if c=='A':
            self.advance = (-19,-12)
            self.press()
        else:
            self.advance = (0,0)
            delta = aoc.dirs4[aoc.dirsArrow[c]]
            self.targetPos = aoc.addPos(self.targetPos, delta)
            
          
    def display(self,surface):
        if self.cToPos == numsToPos:
            targetp = aoc.addPos((32+self.index*keypadWidth,32),aoc.sclPos(64,self.targetPos))
        else:
            targetp = aoc.addPos((32+self.index*keypadWidth,160),aoc.sclPos(64,self.targetPos))
        target = aoc.addPos(targetp,self.advance)
        targetPrev = aoc.addPos(target,lengthArm1)
        
        pos = aoc.addPos(self.pos,self.advance)
        
        if self.advance != (0,0):
            # highlight the cell
            rect = (targetp[0]-20 , targetp[1]-20,40,40)
            surface.fill((180,54,29),rect)
                    
        attach = aoc.addPos(pos,armStartPos)
        attachFront = aoc.subPos(attach,lengthArm2)
        
        shadeCircle(surface,target,10)
        shadeLine(surface,targetPrev,target)
        shadeLine(surface,attachFront,targetPrev)
        shadeCircle(surface,targetPrev,10)
        
        shadeCircle(surface,attachFront,10)
        shadeLine(surface,attach,attachFront)
        
        surface.blit(self.spr.image,pos) 
           

display = aoc.Display(True, keypadWidth * (nbRobot+1), 384, 1 , 0)
sprDirKeypad = aoc.Sprite("dirkeypad")
sprNumKeypad = aoc.Sprite("numkeypad")
sprRobot = aoc.Sprite("robot")
robots = [Robot(sprRobot,i, dirsToPos if i != nbRobot else numsToPos) for i in range(nbRobot+1)]
for i in range(nbRobot):
    robots[i].next = robots[i+1]
result = sequence("539A",nbRobot+1,bestPathsNum)

display.waitKey()
display.waitKey()
display.waitKey()

for c in result:
    robots[0].move(c)
    for i in range(nbRobot):
        img, rect = sprDirKeypad.imageRect()
        display.surface.blit(img,(i*keypadWidth,0),rect) 
    display.surface.blit(sprNumKeypad.image,(nbRobot*keypadWidth,0),rect) 
    for i in range(nbRobot+1):
        robots[i].display(display.surface)
    display.update()

display.waitKey()

