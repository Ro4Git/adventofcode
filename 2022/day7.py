#Advent of code 2022: Day 7
#https://adventofcode.com/2022/day/7
import re, time, copy
from treelib import Node,Tree

class Folder:
    def __init__(self):
        self.fileSizes = 0
        self.subFolderSizes = 0
        self.files = []

    def addFile(self,tokens):
        self.fileSizes += int(tokens[0])
        self.files.append(tokens)


f = open('input_day7.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

tree = Tree()
root = tree.create_node("/","/",data = Folder())
currentNode = root
for line in lines: 
    if line.startswith("$"):
        # its a command
        cmd = line[2:].split(" ")
        if (cmd[0] == "cd"):
            if cmd[1] == "/":
                currentNode = root
            elif cmd[1] == "..":
                currentNode = tree.parent(currentNode.identifier)
            else:
                id = currentNode.identifier + "/" + cmd[1]
                currentNode = tree.get_node(id)
    else:
        #it's a file or dir being listed
        tokens = line.split(" ")
        if tokens[0] == "dir":
            id = currentNode.identifier + "/" + tokens[1]
            dir = tree.create_node(tokens[1],id,parent = currentNode, data = Folder())
        else:
            currentNode.data.addFile(tokens)
tree.show()

def computeFolderSizes(thisNode): 
    thisNode.data.subFolderSizes = thisNode.data.fileSizes
    children = tree.children(thisNode.identifier)
    for node in children:
        thisNode.data.subFolderSizes += computeFolderSizes(node)
    return thisNode.data.subFolderSizes 

totalSize = computeFolderSizes(root)
print(totalSize)


def part1():
    allFolders = 0
    for node in tree.all_nodes():
        if node.data.subFolderSizes <= 100000:
            allFolders += node.data.subFolderSizes
    print(allFolders)
    return 

def part2():
    missingSize = totalSize - 40000000
    smallestFolderSizeToDelete = 40000000
    for node in tree.all_nodes():
        folderSize = node.data.subFolderSizes
        if folderSize >= missingSize and folderSize < smallestFolderSizeToDelete:
            smallestFolderSizeToDelete = folderSize
    print(smallestFolderSizeToDelete)

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