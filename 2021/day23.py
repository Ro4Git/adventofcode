#Advent of code 2021: Day 23
#https://adventofcode.com/2021/day/23
import re, time, copy, sys, math
import astar

f = open('input_day23.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

#hand solved part1

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
#3

#############
#.........CA#
###C#D#D#.###
  #B#A#B#.#
  #########
#303

#############
#.........CA#
###C#D#.#.###
  #B#A#B#D#
  #########
#5303

#############
#.........CA#
###C#.#.#D###
  #B#A#B#D#
  #########
#11303

#############
#.A.......CA#
###C#.#.#D###
  #B#.#B#D#
  #########
#11308

#############
#.A.......CA#
###C#.#.#D###
  #B#B#.#D#
  #########
#11368

#############
#.A........A#
###C#.#.#D###
  #B#B#C#D#
  #########
#11868

#############
#.A........A#
###.#.#C#D###
  #B#B#C#D#
  #########
#12468

#############
#.A........A#
###.#B#C#D###
  #.#B#C#D#
  #########
#12518

#############
#..........A#
###.#B#C#D###
  #A#B#C#D#
  #########
#12521

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
# part1 => 12530

# hand solved part 2:  51872 / too high
# hand solved part 2: 51790 / too high

def printNode(code):
  print("░░░░░░░░░░░░░")  
  print(f"░{code[16:]}░")
  print(f"░░░{code[0]}░{code[4]}░{code[8]}░{code[12]}░░░")
  print(f"  ░{code[1]}░{code[5]}░{code[9]}░{code[13]}░  ")
  print(f"  ░{code[2]}░{code[6]}░{code[10]}░{code[14]}░  ")
  print(f"  ░{code[3]}░{code[7]}░{code[11]}░{code[15]}░  ")
  print("  ░░░░░░░░░")

hallwaypos= [16,17,19,21,23,25,26]
lefts= [[17,16],[19,17,16],[21,19,17,16],[23,21,19,17,16]]
rights= [[19,21,23,25,26],[21,23,25,26],[23,25,26],[25,26]]
distances = {}
# for each pool
for i in range(4):
  column = i * 2 + 18
  for j in range(4):
    d0 = 1 + j
    for k in range(16,27):
      d = d0 + abs(k - column)
      distances[(i*4+j,k)] = d
      distances[(k, i*4+j)] = d


mulFactor = {".":1,"A":1,"B":10,"C":100,"D":1000}

def distanceWithCost(node1,node2):
  pos = [i for i,c in enumerate(node1) if c != node2[i]]
  if len(pos)!=2:
    return 10000000000
  return distances[(pos[0],pos[1])] * mulFactor[node1[pos[0]]] * mulFactor[node1[pos[1]]]

def distanceWithoutCost(node1,node2):
  pos = [i for i,c in enumerate(node1) if c != node2[i]]
  if len(pos)!=2:
    return 10000000000
  return distances[(pos[0],pos[1])]


def heuristic(node,goal):
  return 0

def newNode(node,i,j):
  chars = list(node)
  chars[i], chars[j] = chars[j], chars[i]
  return ''.join(chars)

def neighbours(node):
  #print(node)
  for i in range(4):
    # all valid moves this pool to hallway
    for j in range(4):
      startPos = i*4+j
      if node[startPos] != '.': # first valid letter to move
        # open valid nodes on left
        # open valid nodes on right
        for destPos in lefts[i]:
          if node[destPos] != ".":
            break
          yield newNode(node,startPos,destPos)
        for destPos in rights[i]:
          if node[destPos] != ".":
            break
          yield newNode(node,startPos,destPos)         
        break
    # all valid moves from hallway to this pool
    commonLetter = ""
    j = 0
    while j<4 and node[i*4+j]==".":
      j+=1
    if j == 0:
      continue
    if (j>=4):
     # empty pool
      # this pool can be moved to, check for hallway position that would be valid
      destPos = i*4 + 3
      for startPos in lefts[i]:
        if node[startPos] != ".":
          yield newNode(node,startPos,destPos)
          break
      for startPos in rights[i]:
        if node[startPos] != ".":
          yield newNode(node,startPos,destPos)    
          break   
    else:

      commonLetter = node[i*4+j]
      for k in range(j,4):
        if commonLetter != node[i*4+k]:
          commonLetter = ""
          break
      if commonLetter == "":
        continue
      # this pool can be moved to, check for hallway position that would be valid
      destPos = i*4 + j-1
      for startPos in lefts[i]:
        if node[startPos] != ".":
          if node[startPos] == commonLetter:
            yield newNode(node,startPos,destPos)
          break
      for startPos in rights[i]:
        if node[startPos] != ".":
          if node[startPos] == commonLetter:
            yield newNode(node,startPos,destPos)    
          break   

#############
#...........#
###C#D#D#A###
  #D#C#B#A#
  #D#B#A#C#
  #B#A#B#C#
  #########

source = "CDDBDCBADBABAACC.. . . . .."
target = "AAAABBBBCCCCDDDD.. . . . .."
printNode(target)


def part1():
    return

def part2():
    res = astar.find_path(source,target, neighbors_fnct=neighbours,
                                heuristic_cost_estimate_fnct=heuristic, distance_between_fnct=distanceWithoutCost )
    path = list(res)
    print(path)

    cost = 0
    for i,p in enumerate(path[:-1]):
      printNode(path[i+1])
      cost = cost + distanceWithCost(path[i],path[i+1])
      print(cost)

    print(cost)

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

