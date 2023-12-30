#Advent of code 2023: Day 25
#https://adventofcode.com/2023/day/25
import re, time, copy, math
import networkx as nx
import matplotlib.pyplot as plt

f = open('input_day25.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

graph = nx.Graph()

for line in lines: 
    n1,nodes = line.split(": ")
    for n2 in nodes.split(" "):
        graph.add_edge(n1,n2)

print(graph)
graph.remove_edge("jbz","sqh")
graph.remove_edge("vfj","nvg")
graph.remove_edge("fch","fvh")
print(graph)

res = [graph.subgraph(c).copy() for c in nx.connected_components(graph)]
for subg in res:
    print(subg)

print(len(res[0])*len(res[1]))
#subax1 = plt.subplot(121)
#nx.draw(graph, with_labels=True, font_weight='bold')
#plt.show()  

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