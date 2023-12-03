#Advent of code 2023: Day 2
#https://adventofcode.com/2023/day/2
import re, time, copy

f = open('input_day2.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

#red 0
#green 1
#blue 2


games = []
for line in lines: 
    game = [[s.split(" ") for s in sub] for sub in [subsets.split(", ") for subsets in line.split(": ")[1].split("; ")]]
    print(game)    
    games.append(game)


def part1():
   limits = {"red":12,"green":13,"blue":14}
   validgames = []
   for i,game in enumerate(games):
       valid = True
       for subset in game:
           for cubes in subset:
               if (int(cubes[0]) > limits[cubes[1]]): 
                   valid = False
       if (valid):
           validgames.append(i+1)
   print(sum(validgames))
   return 

def part2():
   powers = []
   for i,game in enumerate(games):
        minimums = {"red":0,"green":0,"blue":0}
        validgames = []
        for subset in game:
            for cubes in subset:
               minimums[cubes[1]] = max(minimums[cubes[1]],int(cubes[0]))
        power = minimums["red"] * minimums["green"] * minimums["blue"]
        powers.append(power)
   print(sum(powers))
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