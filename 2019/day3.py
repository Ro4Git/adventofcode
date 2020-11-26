import copy 
import numpy
import pygame
import itertools

#array of line segment 
#cross all segments with one another and keep the one closest to start point

initial_numbers= []
f = open('input_day3.txt','r')
lines = f.readlines()
wire1 = lines[0].split(",")
wire2 = lines[1].split(",")


def parse_list(wire):
    #return list of rectangles for each segment 
    startx = 0
    starty = 0
    curx = 0
    cury = 0
    segments = []

    for s in wire: 
        direction = s[0]
        length = int(s[1:])
        if direction == 'U':
            cury = cury + length
        elif direction == 'D':
            cury = cury - length
        elif direction == 'R':
            curx = curx + length
        elif direction == 'L':
            curx = curx - length
        segment = pygame.Rect(min(startx,curx),min(starty,cury),abs(startx-curx),abs(starty-cury))
        segments.append(segment)
        startx = curx
        starty = cury
    return segments


def parse_list_distances(wire):
    #return list of rectangles for each segment 
    segments = []
    totaldist = 0
    for s in wire: 
        length = int(s[1:])
        segments.append(totaldist)
        totaldist = totaldist + length
    return segments


def intersect_rect(rect1, rect2):
    #return the distance at which to 
    interx = 0
    intery = 0
    if rect1.w == 0 and rect2.w == 0:
        # 2 vertical lines
        return -1
    elif rect1.h == 0 and rect2.h == 0:
        # 2 horizontal lines
        return -1
    elif rect1.w == 0:
        # 1 vertical, 2 horizontal
        if rect2.left > rect1.left:
            return -1
        if rect2.right < rect1.left:
            return -1
        if rect1.top > rect2.top: 
            return -1
        if rect1.bottom < rect2.top: 
            return -1
        interx = rect1.left
        intery = rect2.top
    else:
        # 2 vertical, 1 horizontal
        if rect1.left > rect2.left:
            return -1
        if rect1.right < rect2.left:
            return -1
        if rect2.top > rect1.top: 
            return -1
        if rect2.bottom < rect1.top: 
            return -1
        interx = rect2.left
        intery = rect1.top
    return abs(interx) + abs(intery)

def intersect_rect_steps(rect1, rect2, prev_rect1, prev_rect2):
    #return the distance at which to 
    stepw1 = 0
    stepw2 = 0
    if rect1.w == 0 and rect2.w == 0:
        # 2 vertical lines
        return -1
    elif rect1.h == 0 and rect2.h == 0:
        # 2 horizontal lines
        return -1
    elif rect1.w == 0:
        # 1 vertical, 2 horizontal
        if rect2.left > rect1.left:
            return -1
        if rect2.right < rect1.left:
            return -1
        if rect1.top > rect2.top: 
            return -1
        if rect1.bottom < rect2.top: 
            return -1

        stepw1 = rect2.top - prev_rect1.bottom
        stepw2 = rect1.left - prev_rect2.left
    else:
        # 2 vertical, 1 horizontal
        if rect1.left > rect2.left:
            return -1
        if rect1.right < rect2.left:
            return -1
        if rect2.top > rect1.top: 
            return -1
        if rect2.bottom < rect1.top: 
            return -1
        stepw1 = rect2.left - prev_rect1.left
        stepw2 = rect1.bottom - prev_rect2.bottom
    return abs(stepw1) + abs(stepw2)


segments1 = parse_list(wire1)
segments2 = parse_list(wire2)
distances1 = parse_list_distances(wire1)
distances2 = parse_list_distances(wire2)

print(distances1)
print(distances2)
min_dist = 1000000000
prev_seg1 = pygame.Rect(0,0,0,0)
prev_seg2 = pygame.Rect(0,0,0,0)
for seg1, dist1 in itertools.izip(segments1,distances1):
    for seg2, dist2 in itertools.izip(segments2,distances2):
        dist = intersect_rect_steps(seg1, seg2, prev_seg1, prev_seg2)
        # distance so far in wire1 and wire2 
        if (dist>=0):
            totaldist = dist1 + dist2 + dist
            if (totaldist>0): 
                if (totaldist < min_dist ):
                    min_dist = totaldist
                print totaldist
        prev_seg2 = seg2
    prev_seg1 = seg1
print min_dist        



