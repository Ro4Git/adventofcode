#Advent of code 2023: Day 20
#https://adventofcode.com/2023/day/20
import re, time, copy, math, numpy
import json

f = open('input_day20.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

modules = {}

class Broadcaster:
    def __init__(self, name, targets):
        self.targets = targets 
        self.name = name
    def reset(self):
        return    
    def addInput(self, input):
        return
    def processPulse(self,moduleFrom,value):
        toProcess = []
        for target in self.targets:
           toProcess.append((target,self.name,value))
        return toProcess
    
class EndNode:
    def __init__(self, name):
        self.name = name
        self.pulses = [0,0]
    def reset(self):
        self.pulses = [0,0]
        return    
    def addInput(self, input):
        return    
    def processPulse(self,moduleFrom,value):
        self.pulses[value] += 1
        return []    
    
class FlipFlop:
    def __init__(self, name, targets):
        self.targets = targets 
        self.name = name
        self.state = 0
    def addInput(self, input):
        return      
    def reset(self):
        self.state = 0
        return    
    def processPulse(self,moduleFrom,value):
        if value != 1:
            toProcess = []
            self.state = (self.state + 1) & 1
            for target in self.targets:
                toProcess.append((target,self.name,self.state))
            return toProcess
        return []

class Conjunction:
    def __init__(self, name, targets):
        self.targets = targets 
        self.name = name
        self.memory = {}
    def addInput(self, input):
        self.memory[input] = 0
        return
    def reset(self):
        for k,v in self.memory.items():
            v = 0
        return    
    def processPulse(self,moduleFrom,value):
        toProcess = []
        self.memory[moduleFrom] = value
        # check if all inputs have same state
        allInputsValue = sum(state for state in self.memory.values())        
        if allInputsValue == len(self.memory.values()):
            for target in self.targets:
                toProcess.append((target,self.name,0))      
        else:
            for target in self.targets:
                toProcess.append((target,self.name,1))      
        return toProcess

for line in lines: 
    nameCode,dests = line.split(" -> ")
    type = nameCode[0]
    destLists = [dests]
    if "," in dests: 
        destLists = [d for d in dests.split(", ")]

    if type == '&':
         modules[nameCode[1:]] = Conjunction(nameCode[1:],destLists)
    elif type == '%':
        modules[nameCode[1:]] = FlipFlop(nameCode[1:],destLists)
    else:
        modules[nameCode] = Broadcaster(nameCode,destLists)
    
toAdd = []
for module in modules.values():
    for target in module.targets:
        if not target in modules:
            toAdd.append(target)
        else:
            modules[target].addInput(module.name)
        
for name in toAdd:
    modules[name] = Broadcaster(target,[])

def pressButton():
    toProcess = [("broadcaster","button",0)]
    nbPulse = [0,0]
    while len(toProcess):
        target,source,value = toProcess.pop(0)
        nbPulse[value] += 1
        currentModule = modules[target]
        toProcess.extend(currentModule.processPulse(source,value))
    return nbPulse

toDetect = {"qq":0,"ls":0,"bg":0,"sj":0}
def pressButton_part2(currentIter):
    global toDetect
    toProcess = [("broadcaster","button",0)]
    nbPulse = [0,0]
    while len(toProcess):
        target,source,value = toProcess.pop(0)
        nbPulse[value] += 1
        currentModule = modules[target]
        toProcess.extend(currentModule.processPulse(source,value))
        if currentModule.name == "kz":
            for k,v in toDetect.items():
                if currentModule.memory[k] == 1:
                    if v == 0:
                        toDetect[k] = currentIter            
                        print(currentIter,toDetect)
                    else:
                        if currentIter % v != 0:
                            print("error loop value")
    return nbPulse

def part1():
    nbPulses = [0,0]
    for i in range(1000):
        pulses = pressButton()
        nbPulses[0] += pulses[0]
        nbPulses[1] += pulses[1]
    print(nbPulses)
    print(nbPulses[0]*nbPulses[1])

def part2():
#specific data from my example : rx will be triggered by kz conjuction (when all of qq,ls,bg and sj are high)
#    &qq -> kz
#   &ls -> kz
#   &kz -> rx
#   &bg -> kz
#    &sj -> kz
#   check for loops in these modules to find lcm

    for module in modules.values():
        module.reset()
    rxModule = EndNode("rx")
    modules["rx"] = rxModule
    nbButtonPressed = 0
    muls = 0
    while muls == 0:
        rxModule.reset()
        nbButtonPressed +=1
        pressButton_part2(nbButtonPressed)
        muls = toDetect["qq"] * toDetect["ls"] * toDetect["bg"] * toDetect["sj"]

    print("")
    print(muls)
    # all results are prime so no need to do lcm
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