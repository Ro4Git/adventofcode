#Advent of code 2022: Day 2
#https://adventofcode.com/2022/day/2
import re, time, copy

f = open('input_day2.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

points = {}


def part1():
    points["A X"] = 4 
    points["A Y"] = 8
    points["A Z"] = 3
    points["B X"] = 1
    points["B Y"] = 5
    points["B Z"] = 9
    points["C X"] = 7
    points["C Y"] = 2
    points["C Z"] = 6
    gamePoints= [points[line] for line in lines]
    totalPoints = sum(gamePoints)

    print(totalPoints)
    return 

# X = loose
# Y = draw
# Z = win

def part2():
    points["A X"] = 3
    points["A Y"] = 4
    points["A Z"] = 8
    points["B X"] = 1
    points["B Y"] = 5
    points["B Z"] = 9
    points["C X"] = 2
    points["C Y"] = 6
    points["C Z"] = 7
    gamePoints= [points[line] for line in lines]
    totalPoints = sum(gamePoints)

    print(totalPoints)
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