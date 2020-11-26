import copy 
import itertools
import time


def add(v,w):
    x,y,z = v
    X,Y,Z = w
    return (x+X, y+Y, z+Z)

def gravPull(a,b):
    return 1 if a>b else -1 if a<b else 0

def gravity(v,w):
    x,y,z = v
    X,Y,Z = w
    return (gravPull(x,X),gravPull(y,Y),gravPull(z,Z))

def engery(v):
    x,y,z = v
    return abs(x) + abs(y) + abs(z)


def test_program():

    start_time = time.time()
    print("---------- Starting --------")


    moon_pos = [(-7,-1,6),(6,-9,-9),(-12,2,-7),(4,-17,-12)]
    moon_vel = [(0,0,0),(0,0,0),(0,0,0),(0,0,0)]

    # test sample 
    #moon_pos = [(-8,-10,0),(5, 5,10),(2,-7,3),(9,-8,-3)]
    #moon_pos = [(-1,0,2),(2, -10,-7),(4,-8,8),(3,5,-1)]
    initial_pos = copy.copy(moon_pos)
    initial_vel = copy.copy(moon_vel)

    previous_state = []
    nbsteps = 5000  
    i = 0
    while True:
        if (i%100000)==0:
            print("step {0}\r".format(i), end='\r')

        for a in range(4):
            for b in range(a+1,4):
                    deltax = 1 if moon_pos[b][0]>moon_pos[a][0] else -1 if moon_pos[b][0]<moon_pos[a][0] else 0
                    deltay = 1 if moon_pos[b][1]>moon_pos[a][1] else -1 if moon_pos[b][1]<moon_pos[a][1] else 0
                    deltaz = 1 if moon_pos[b][2]>moon_pos[a][2] else -1 if moon_pos[b][2]<moon_pos[a][2] else 0
                    moon_vel[a] = (moon_vel[a][0] + deltax,moon_vel[a][1] + deltay,moon_vel[a][2] + deltaz)
                    moon_vel[b] = (moon_vel[b][0] - deltax,moon_vel[b][1] - deltay,moon_vel[b][2] - deltaz)
        
        

        for a in range(4):
            moon_pos[a] = (moon_pos[a][0] +  moon_vel[a][0],moon_pos[a][1] +  moon_vel[a][1],moon_pos[a][2] +  moon_vel[a][2])
            #print("pos=<x= {0:3}, y= {1:3}, z=  {2:3}>, vel=<x=  {3:3}, y=  {4:3}, z=  {5:3}>".format(moon_pos[a][0],moon_pos[a][1],moon_pos[a][2],moon_vel[a][0],moon_vel[a][1],moon_vel[a][2]))

        #if (moon_pos == initial_pos):
        #     print("Cycle on pos reached at step {1}".format(b,i+1))
        #if (moon_vel == initial_vel):
        #     print("Cycle on vel reached at step {1}".format(b,i+1))


        for b in range(3):
            allEqual = 1
            for a in range(4):
                if (moon_pos[a][b] != initial_pos[a][b] or moon_vel[a][b] != initial_vel[a][b]):
                    allEqual = 0
                    break
            if (allEqual):
                print("Cycle on coord {0} reached at step {1}".format(b,i+1))



        if (moon_pos == initial_pos and moon_vel == initial_vel):
            print("Initial state found: {0}".format(i+1))
            break
        i += 1


    sum_energy = 0
    for pos,vel in zip(moon_pos,moon_vel):
        pot = engery(pos)
        kin = engery(vel)
        sum_energy += pot *  kin

    #print(sum_energy)


test_program()


