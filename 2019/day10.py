import copy 
import itertools
import time



import math



def angle(vector1, vector2):
    ang = math.atan2(vector2[1], vector2[0]) - math.atan2(vector1[1], vector1[0])
    if (ang < 0 ):
        ang += math.pi * 2
    return ang 
 

#def angle(vector1, vector2):
#    x1, y1 = vector1
#    x2, y2 = vector2
#    inner_product = x1*x2 + y1*y2
#    len1 = math.hypot(x1, y1)
#    len2 = math.hypot(x2, y2)
#    #if (len1 == 0 or len2 == 0):
#    #    print("error vector {0} - {1}".format(vector1,vector2))
#    return math.acos(inner_product/(len1*len2))

def dot(v,w):
    x,y = v
    X,Y = w
    return x*X + y*Y

def length(v):
    x,y = v
    return math.sqrt(x*x + y*y)

def vector(b,e):
    x,y = b
    X,Y = e
    return (X-x, Y-y)

def unit(v):
    x,y = v
    mag = length(v)
    return (x/mag, y/mag)

def distance(p0,p1):
    return length(vector(p0,p1))

def scale(v,sc):
    x,y = v
    return (x * sc, y * sc)

def add(v,w):
    x,y = v
    X,Y = w
    return (x+X, y+Y)


# Given a line with coordinates 'start' and 'end' and the
# coordinates of a point 'pnt' the proc returns the shortest 
# distance from pnt to the line and the coordinates of the 
# nearest point on the line.
#
# 1  Convert the line segment to a vector ('line_vec').
# 2  Create a vector connecting start to pnt ('pnt_vec').
# 3  Find the length of the line vector ('line_len').
# 4  Convert line_vec to a unit vector ('line_unitvec').
# 5  Scale pnt_vec by line_len ('pnt_vec_scaled').
# 6  Get the dot product of line_unitvec and pnt_vec_scaled ('t').
# 7  Ensure t is in the range 0 to 1.
# 8  Use t to get the nearest location on the line to the end
#    of vector pnt_vec_scaled ('nearest').
# 9  Calculate the distance from nearest to pnt_vec_scaled.
# 10 Translate nearest back to the start/end line. 
# Malcolm Kesson 16 Dec 2012

def pnt2line(pnt, start, end):
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)    
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    #nearest = add(nearest, start)
    return dist


point_list = []
initial_grid= []
f = open('input_day10.txt','r')
coordy = 0
for line in f:
    initial_grid.append(line)
    coordx = 0
    for c in line:
        if (c =='#'):
            point_list.append([coordx,coordy])
        coordx += 1
    coordy += 1

    
print(point_list)
print(len(point_list))

nbvisibility = []
maxviz = 0
maxindex = 0
i = 0


start_time = time.time()
print("---------- Starting --------")

if (False): # part 1
    for segA in point_list:
        nbviz = 0
        for segB in point_list: 
            if (segB != segA):
                visible = True       
                for pt2 in point_list:
                    if (pt2 != segA and pt2 != segB):
                        los = distPnt2segment(pt2,segA,segB)
                        if (los <= 0.001):
                            #segB cannot be seen from segA
                            visible = False
                            break
                if visible:
                    nbviz += 1      
        nbvisibility.append(nbviz)
        if (nbviz > maxviz):
            maxviz = nbviz
            maxindex = i
            print("--- new max found : {0}".format(maxviz))
        i += 1 



#part 2 
start_pt = [11,19] #point_list[270]
print(len(point_list))
point_list.remove(start_pt)
print(len(point_list))
num_destoyed = 0
current_dir = [0,-1]

for n in range(200):
    # find closest satellite to destroy
    to_destroy = []
    closest = 1000.0
    for pt0 in point_list:
        v = vector(start_pt,pt0)
        if (abs(angle(current_dir,v)) <= 0.00001):
            l = length(v)
            if (l < closest):
                to_destroy = pt0
                closest = l
    point_list.remove(to_destroy)
    print("{2}: destroying {0}/{1}".format(to_destroy,len(point_list),n))

    # find next satellite 
    closest_angle = 1000
    picked_next_point = []
    for pt0 in point_list:
        v = vector(start_pt,pt0)
        anglev = angle(current_dir,v)
        if (anglev > 0.00001 and anglev < closest_angle):
            new_current_dir = v
            closest_angle = anglev
            picked_next_point = pt0
    if (len(picked_next_point) ==0):
       for pt0 in point_list:
        v = vector(start_pt,pt0)
        anglev = angle(current_dir,v)
        print(anglev)

    current_dir = new_current_dir
    print(closest_angle, picked_next_point)

print("------ Result -------")

#[11, 19]
# point 270
print("--- {0:.3f} seconds ---".format((time.time() - start_time)))

