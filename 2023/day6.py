#Advent of code 2023: Day 6
#https://adventofcode.com/2023/day/6
import re, time, copy, math

f = open('input_day6.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

# skipping reading and hardcoding values
#Time:        55     82     64     90
#Distance:   246   1441   1012   1111
races = [[55,246],[82,1441],[64,1012],[90,1111]]

def distIfTime(waitTime,raceTime):
    speed = waitTime
    dist = (raceTime - waitTime) * speed
    return dist

# brute force approach 
def numWays(raceTime,maxDist):
    num = 0
    for i in range(raceTime):
        if distIfTime(i,raceTime) > maxDist:
            num = num + 1
    return num

def smarter_NumWays(raceTime,maxDist):
    # smarter way would be to solve the 2 
    # roots of  dist = - x^2 + x.rt - maxDist (x = waitTime) 
    # ( this is a parabol that goes over 0 between the 2 roots)
    # roots = -b +/- sqrt(delta)/2a , delta = b*b - 4ac
    # a = -1 , b = raceTime , c = -maxDist
    delta = raceTime*raceTime - 4 * (-1) * (-maxDist)
    r1 = raceTime - math.sqrt(delta) / (-2.0 )  
    r2 = raceTime + math.sqrt(delta) / (-2.0 )  
    first = math.ceil(r2)
    second = math.floor(r1)
    return 1 + second - first


def part1():
    numWaysRaces = [numWays(race[0],race[1]) for race in races]
    print(numWaysRaces)
    numWaysRaces = [smarter_NumWays(race[0],race[1]) for race in races]
    print(numWaysRaces)
    mul = 1
    for m in numWaysRaces:
        mul = mul * m
    print(mul)    
    return 


def part2():
    print(smarter_NumWays(55826490,246144110121111))
    print(numWays(55826490,246144110121111))
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