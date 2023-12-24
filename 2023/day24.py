#Advent of code 2023: Day 24
#https://adventofcode.com/2023/day/24
import re, time, copy, math
from sympy import Symbol
from sympy import solve_poly_system

f = open('input_day24.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

rays = []
for line in lines:
    pos,dir = line.split(" @ ")
    rays.append ( ( tuple(int(n) for n in pos.split(", ")) , tuple(int(n) for n in dir.split(", ")) ) )

def intersect2D(ray1, ray2):
    xdiff = (-ray1[1][0] , -ray2[1][0])
    ydiff = (-ray1[1][1] , -ray2[1][1])
 
    def add2D(pos,delta):
        return (pos[0]+delta[0],pos[1]+delta[1])
    def sub2D(pos1,pos2):
        return (pos2[0]-pos1[0],pos2[1]-pos1[1])
    def dot(v1,v2):
        return v1[0]*v2[0] + v1[1]*v2[1]

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None
    p1 = add2D(ray1[0],ray1[1]) 
    p2 = add2D(ray2[0],ray2[1]) 
    d = (det(ray1[0],p1), det(ray2[0],p2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div  
    sign1 = dot(ray1[1],sub2D(ray1[0],(x,y)))
    sign2 = dot(ray2[1],sub2D(ray2[0],(x,y)))
    if sign1<0 or sign2<0:
        return None
    return (x, y)

def part1():
    limits = [200000000000000,400000000000000]
    #limits = [7,27]
    nbInLimits = 0 
    for i,ray1 in enumerate(rays):
        for j in range(i+1,len(rays)):
            pos = intersect2D(ray1,rays[j])
            if pos and pos[0] >= limits[0] and pos[0] <= limits[1] and pos[1] >= limits[0] and pos[1] <= limits[1]:
                nbInLimits += 1
    print(nbInLimits)
    return 

def part2():
    # unknowns
    x,y,z = [Symbol('x'),Symbol('y'),Symbol('z')]
    vx,vy,vz = [Symbol('vx'),Symbol('vy'),Symbol('vz')]
    t = [Symbol('t0'),Symbol('t1'),Symbol('t2')]

    # equations, take first 3 rays as should be enough to solve unknowns
    equations = []
    for i,ray in enumerate(rays[:3]):
        equations.append((x + vx*t[i]) - (ray[0][0] + ray[1][0]*t[i]))
        equations.append((y + vy*t[i]) - (ray[0][1] + ray[1][1]*t[i]))
        equations.append((z + vz*t[i]) - (ray[0][2] + ray[1][2]*t[i]))
   
    # solve all 9 equations to get rock pos, velocity and times
    res = solve_poly_system(equations,x,y,z,vx,vy,vz,t[0],t[1],t[2])
    
    print(res)
    print(res[0][0]+res[0][1]+res[0][2]) 
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