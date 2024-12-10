#Advent of code 2024: Day 9
#https://adventofcode.com/2024/day/9
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc

lines = aoc.ReadPuzzleInput("input_day9.txt")
diskmap = list(lines[0])

class Chunk:
    def __init__(self, pos, id, length):
        self.pos = pos
        self.id = id
        self.length = length 
        
    def split(self, splitIndex):
        if splitIndex == 0 or splitIndex == self.length:
            print("error")
            return self
        return Chunk(self.pos, self.id, splitIndex),Chunk(self.pos+splitIndex,self.id, self.length - splitIndex)

    def checksum(self):
        checksum = 0
        if (self.id >0):
            for i in range(self.pos,self.pos+self.length):
                checksum += self.id * i
        return checksum

chunks = []    
files = []
freeSpaces = []
currentIndex = 0

for i,c in enumerate(diskmap): 
    chunklength = int(c)
    if (chunklength >0):
        chunkData = Chunk(currentIndex,i//2 if ((i % 2)==0) else -1,chunklength)
        currentIndex += chunklength
        chunks.append(chunkData)
        if (i % 2) == 0: 
            files.append(chunkData)
        else: 
            freeSpaces.append(chunkData)
            
maxLength = currentIndex
            

def defragment(files, freeSpaces):
# move parts of files to every free spots 
    currentFile = files.pop()
    currentFree = freeSpaces.pop(0)
    newFiles = []
    while currentFree != None and currentFree.pos < currentFile.pos:
        if currentFile.length == currentFree.length: 
            newFiles.append(Chunk(currentFree.pos, currentFile.id, currentFile.length))
            currentFile = files.pop()
            currentFree = freeSpaces.pop(0) if len(freeSpaces)>0 else None
        elif currentFile.length < currentFree.length: 
            newFile, newFree = currentFree.split(currentFile.length)
            newFile.id = currentFile.id
            currentFree = newFree
            newFiles.append(newFile)
            currentFile = files.pop()
        elif currentFile.length > currentFree.length: 
            newFile1, newFile2 = currentFile.split(currentFile.length - currentFree.length)
            newFile2.pos = currentFree.pos
            newFiles.append(newFile2)
            currentFree = freeSpaces.pop(0) if len(freeSpaces)>0 else None
            currentFile = newFile1   
            
        result = files.copy()
        result.extend(newFiles)
        result.append(currentFile)  
    return result

def defragment2(files, freeSpaces):
# find first free spot to move the entire file
    for chunk in reversed(files): 
        for i,freeChunk in enumerate(freeSpaces):
            if freeChunk.pos + freeChunk.length > chunk.pos:
                break
            if freeChunk.length >= chunk.length:
                chunk.pos = freeChunk.pos
                freeChunk.pos += chunk.length
                freeChunk.length -= chunk.length
                if (freeChunk.length == 0): 
                    freeSpaces.pop(i)
                break
    return files
         
              
def part1():
    newFiles = defragment(files.copy(),freeSpaces.copy())    
    checksum = sum([c.checksum() for c in newFiles])
    print(checksum)
    return 

def part2():
    newFiles = defragment2(files.copy(),freeSpaces.copy())    
    checksum = sum([c.checksum() for c in newFiles])
    print(checksum)
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

