#Advent of code 2021: Day 23
#https://adventofcode.com/2021/day/23
import re, time, copy, sys, math, pygame
from collections import defaultdict
from functools import reduce,cmp_to_key
from itertools import combinations, combinations_with_replacement

f = open('input_day23.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

#############
#...........#
###C#D#D#A###
  #B#A#B#C#
  #########


#############
#..........A#
###C#D#D#.###
  #B#A#B#C#
  #########
3

#############
#.........CA#
###C#D#D#.###
  #B#A#B#.#
  #########
303

#############
#.........CA#
###C#D#.#.###
  #B#A#B#D#
  #########
5303

#############
#.........CA#
###C#.#.#D###
  #B#A#B#D#
  #########
11303

#############
#.A.......CA#
###C#.#.#D###
  #B#.#B#D#
  #########
11308

#############
#.A.......CA#
###C#.#.#D###
  #B#B#.#D#
  #########
11368

#############
#.A........A#
###C#.#.#D###
  #B#B#C#D#
  #########
11868

#############
#.A........A#
###.#.#C#D###
  #B#B#C#D#
  #########
12468

#############
#.A........A#
###.#B#C#D###
  #.#B#C#D#
  #########
12518

#############
#..........A#
###.#B#C#D###
  #A#B#C#D#
  #########
12521

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
12530



#############
#...........#
###C#D#D#A###
  #D#C#B#A#
  #D#B#A#C#
  #B#A#B#C#
  #########

#############
#A.........A#
###C#D#D#.###
  #D#C#B#.#
  #D#B#A#C#
  #B#A#B#C#
  #########


#############
#AC.......CA#
###C#D#D#.###
  #D#C#B#.#
  #D#B#A#.#
  #B#A#B#.#
  #########


#############
#AC.......CA#
###C#.#.#.###
  #D#C#B#.#
  #D#B#A#D#
  #B#A#B#D#
  #########


def part1():
    return

def part2():
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

