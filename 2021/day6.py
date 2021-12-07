#Advent of code 2021: Day 6
#https://adventofcode.com/2021/day/6
import re, time, copy

f = open('input_day6.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

#           *               *             
# 0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 3 3 3 3
#                     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3  
#--------------------------------------------------------------------
# 5 4 3 2 1 0 6 5 4 3 2 1 0 6 5 4 3 2 1 0 6 5 4 3 2 1 0 6 5 4 3 2 1 0 
#--------------------------------------------------------------------
#             8 7 6 5 4 3 2 1 0 6 5 4 3 2 1 0 6 5 4 3 2 1 0 6 5 4 3 2  gen 1
#                           8 7 6 5 4 3 2 1 0 6 5 4 3 2 1 0 6 5 4 3 2  gen 12
#                                         8 7 6 5 4 3 2 1 0 6 5 4 3 2  gen 13
#                                                       8 7 6 5 4 3 2  gen 14
#------------------------gen 1 --------------------------------------
#                               8 7 6 5 4 3 2 1 0 6 5 4 3 2 1 0 6 5 4  
#                                             8 7 6 5 4 3 2 1 0 6 5 4 
#                                                           8 7 6 5 4
#------------------------gen 12 -------------------------------------- 
#                                             8 7 6 5 4 3 2 1 0 6 5 4 
#                                                           8 7 6 5 4                                



starting_fish = [int(n) for n in lines[0].split(',')]

# brute force approach
def iteration(list_in):
    new_gen =  [8 for x in list_in if x==0]
    decrease = [x-1 if x>0 else 6 for x in list_in]
    return decrease + new_gen

def nbforX(num,X):
    loop_list = [num]
    for i in range(X):
        loop_list = iteration(loop_list)
    return len(loop_list)

test_dict_80 = {}
for i in range(5):
    test_dict_80[i+1] = nbforX(i+1,80)
print(test_dict_80)

# doesn't scale
#test_dict_256 = {}
#for i in range(5):
#    print(i)
#    test_dict_256[i+1] = nbforX(i+1,256)
# print(test_dict_256)


def part1():
    nums = [test_dict_80[x] for x in starting_fish]
    print(sum(nums))
    return 

def part2():
#    nums = [test_dict_256[x] for x in starting_fish]
    nbs = [starting_fish.count(i) for i in range(9)]
    for i in range(256):
        nbnewfish = nbs[0]
        nbs = nbs[1:] + nb[nbnewfish]
        nbs[6] += nbnewfish
    print(sum(nbs))
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