#Advent of code 2024: Day 23
#https://adventofcode.com/2024/day/23
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc
import networkx as nx


lines = aoc.ReadPuzzleInput("input_day23.txt")
computers = aoc.ToList(lines,'-')

graph = nx.Graph()
for comp in computers: 
    graph.add_edge(comp[0],comp[1])

#print(graph)

def part1():
    validCliques = []
    for clique in nx.enumerate_all_cliques(graph):
        if len(clique) == 3:
            for n in clique:
               if n.startswith("t"):
                    validCliques.append(clique)
                    break
    print(len(validCliques))
    return 

def part2():
    largest_clique = [clique for clique in nx.enumerate_all_cliques(graph)][-1]
    code = ",".join(sorted(largest_clique))
    print(code)    
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

