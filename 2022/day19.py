#Advent of code 2022: Day 19
#https://adventofcode.com/2022/day/19
import re, time, copy, functools
from collections import deque

f = open('input_day19.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

temp = [re.findall(r"\d+",line) for line in lines]
#Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 14 clay. Each geode robot costs 2 ore and 16 obsidian.
maxTime = 24

class Blueprint:

    def __init__(self,tokens):
        if (type(tokens) == list):
            self.robotsCosts = []
            self.robotsCosts.append((int(tokens[1]),0,0)) # oreRobot
            self.robotsCosts.append((int(tokens[2]),0,0)) # clayRobot
            self.robotsCosts.append((int(tokens[3]),int(tokens[4]),0)) #obsRobot
            self.robotsCosts.append((int(tokens[5]),0,int(tokens[6]))) #geoRobot
            self.maxResCost4Robots = [*[max(res) for res in zip(*self.robotsCosts)],0]
            self.resources = [0]*4
            self.robots = [1,0,0,0]
            self.remainingTime = maxTime
        else:
            self.robotsCosts = tokens.robotsCosts
            self.maxResCost4Robots = tokens.maxResCost4Robots
            self.resources = copy.deepcopy(tokens.resources)
            self.robots = copy.deepcopy(tokens.robots)
            self.remainingTime = copy.deepcopy(tokens.remainingTime)            

    def maxGeodes(self):
        # at this stage, how many geode can you produce if no more robots are created
        return self.resources[3] + self.remainingTime * self.robots[3]

    def potentialMaxGeodes(self):
        # at this stage, how many geode can you produce if no more robots are created
        # and you would build 1 Geode robot every frame
        return self.resources[3] + self.remainingTime * self.robots[3] + (self.remainingTime * (self.remainingTime-1))//2

    def canBuild(self,robotIndex):
        for resIndex in range(3):
            if self.robotsCosts[robotIndex][resIndex]> self.resources[resIndex]:
                return False
        return True

    def couldEventuallyBuild(self,robotIndex):
        for resIndex in range(3):
            if self.robotsCosts[robotIndex][resIndex]>0 and self.robots[resIndex] == 0:
                return False
        return True

    def nexts(self):
        for robotType in range(4): 
            if self.maxResCost4Robots[robotType] and self.robots[robotType] * self.remainingTime + self.resources[robotType]  >= self.maxResCost4Robots[robotType] * self.remainingTime:
                continue
            if not self.couldEventuallyBuild(robotType):
                #not possible to produce required resources for resType robot
                continue
            #how long             
            requiredTime = 1 + (max(0 if disp>=needed else (needed - disp + prod -1) // prod
                                    for needed, disp,prod in zip(self.robotsCosts[robotType],self.resources,self.robots) if needed))
            if requiredTime < self.remainingTime:
                newPrint = Blueprint(self)
                for resIndex in range(3):
                    newPrint.resources[resIndex] +=  newPrint.robots[resIndex] * requiredTime - newPrint.robotsCosts[robotType][resIndex] 
                newPrint.resources[3] +=  newPrint.robots[3] * requiredTime 
                newPrint.robots[robotType] += 1
                newPrint.remainingTime = self.remainingTime - requiredTime
                yield Blueprint(newPrint)


def findBestPath(n1):
    candidates = deque([n1])
    visited = {}
    currentMax = 0
    iterCount = 0
    maxTest = None
    while candidates:
        candidate = candidates.popleft()
        for next in candidate.nexts():
            if next in visited: 
                continue
            if next.potentialMaxGeodes() <= currentMax:
                continue
            iterCount += 1
            geoMax = next.maxGeodes()
            if (geoMax > currentMax):
                currentMax = geoMax
                maxTest = next
            visited[next]= True
            candidates.append(next)
    return maxTest



def part1():
    global maxTime
    maxTime = 24
    blueprints = [Blueprint(tokens) for tokens in temp]
    value = 0
    for i,blueprint in enumerate(blueprints):
        res = findBestPath(blueprint)
        if (res != None):
            print("Blueprint ",i,": " , res.maxGeodes(), res.resources,res.remainingTime,res.robots)
            value += res.maxGeodes() * (i+1)
        else:
            print("Blueprint ",i,": 0")
    print(value)
    return


def part2():
    global maxTime
    maxTime = 32
    blueprints = [Blueprint(tokens) for tokens in temp]
    value = 1
    for blueprint in blueprints[:3]:
        res = findBestPath(blueprint)
        if (res != None):
            print("Blueprint :" , res.maxGeodes(), res.resources,res.remainingTime,res.robots)
            value *= res.maxGeodes()
        else:
            print("Blueprint : 0")
    print(value)
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
