#Advent of code 2024: Day 24
#https://adventofcode.com/2024/day/24
import re, time, copy , functools, itertools
from collections import defaultdict
import aoc
import random

lines = aoc.ReadPuzzleInput("input_day24.txt")
sections = aoc.ToSections(lines)
inputs = {a:int(b) for a,b in aoc.ToList(sections[0],': ')}

operations =  {op[1]:tuple(op[0].split(' ')) for op in aoc.ToList(sections[1],' -> ')}
print(inputs)
print(operations)

def doOp(a, op, b):
    if op == "AND":
        return a & b
    elif op == "OR":
        return a | b
    elif op == "XOR":
        return a ^ b

def eval(results, x):
    if x in results:
        return results[x]
    op = operations[x]
    results[x] = doOp(eval(results,op[0]),op[1],eval(results,op[2]))
    return results[x]

valueColors = {-1:(77,77,69), 0:(198,94,25),1:(156,198,25)}
valueImgs = {-1:aoc.pygame.image.load("images/bitnone.png"),0:aoc.pygame.image.load("images/bit0.png"),1:aoc.pygame.image.load("images/bit1.png")}
coordImgs = {"X":aoc.pygame.image.load("images/bitX.png"),"Y":aoc.pygame.image.load("images/bitY.png"),"Z":aoc.pygame.image.load("images/bitZ.png")}
backgroundColor = (140,140,140)
headerColor = (160,160,160)
sepColor = (120,120,120)
progressMax = 50


class ConnexionPoint:
    def __init__(self,name,pos):
        self.name = name
        self.pos = pos
        self.val = -1
    def draw(self,surface, offset):
        pos = aoc.addPos(self.pos,offset)
        aoc.pygame.draw.circle(surface,valueColors[self.val],pos,3)
        aoc.pygame.draw.circle(surface,sepColor,pos,3,width = 1)

def drawProgressLine(surface,pt1,pt2,col1,col2,progress):
    midPoint = aoc.addPos(pt1, aoc.sclPos(progress , aoc.subPos(pt2,pt1)))
    aoc.pygame.draw.line(surface,col1,pt1,midPoint,width = 3)
    aoc.pygame.draw.line(surface,col2,midPoint,pt2,width = 2)

class ConnexionLine:
    def __init__(self,pt1,pt2):
        self.pt1 = pt1
        self.pt2 = pt2
        self.step = 0
    
    def update(self):
        if self.pt1.val != self.pt2.val:
            self.step += 1
            if self.step >= progressMax:
                self.pt2.val = self.pt1.val
                
        
    def draw(self,surface,offset):
        pos1 = aoc.addPos(self.pt1.pos,offset)
        pos2 = aoc.addPos(self.pt2.pos,offset)
        
        if self.pt1.val == self.pt2.val:
            color = valueColors[self.pt1.val]
            if pos2 < pos1:
                tmp1 = aoc.addPos(pos1,(3,0))
                tmp2 = (tmp1[0],pos2[1])
                aoc.pygame.draw.line(surface,color,tmp1,tmp2,width = 2)
                aoc.pygame.draw.line(surface,color,tmp2,pos2,width = 2)
            else:
                aoc.pygame.draw.line(surface,color,pos1,pos2,width = 2)
        else:
            color1 = valueColors[self.pt1.val]
            color2 = valueColors[self.pt2.val]
            if pos2 < pos1:
                tmp1 = aoc.addPos(pos1,(3,0))
                tmp2 = (tmp1[0],pos2[1])
                h = tmp2[1] - tmp1[1]
                w = tmp2[0] - pos2[0]
                progress= self.step/progressMax 
                substep = h/(w+h)
                if (progress < substep):
                    # progress in first part
                    # [ ------ h ----- ][--------------- w -----------]
                    # [           s/ (h+w)
                    # [           s                                   ] 
                    drawProgressLine(surface,tmp1,tmp2,color1,color2,progress * (w+h)/h)  
                    aoc.pygame.draw.line(surface,color2,tmp2,pos2,width = 2)
                else:
                    aoc.pygame.draw.line(surface,color1,tmp1,tmp2,width = 3)
                    drawProgressLine(surface,tmp2,pos2,color1,color2,(progress - substep) * (w+h)/w)  
            else:
                drawProgressLine(surface,pos1,pos2,color1,color2,self.step/progressMax)            
        

class Gate:
    def __init__(self,op,in1,in2,out,pos):
        self.img = aoc.pygame.image.load("images/gate_"+op+".png").convert_alpha()
        self.op = op
        self.pos = pos
        self.inputs = [in1,in2]
        self.out = out
        self.outVal = -1
        self.conPoints = {in1:ConnexionPoint(in1,aoc.addPos((0,8),self.pos)),in2:ConnexionPoint(in2,aoc.addPos((0,40),self.pos)),out:ConnexionPoint(out,aoc.addPos((48,24),self.pos))}
    def getConPoint(self,name):
        return self.conPoints.get(name)
    
    def update(self):
        v1 = self.conPoints[self.inputs[0]].val
        v2 = self.conPoints[self.inputs[1]].val
        if v1 >= 0 and v2 >= 0:
            res = doOp(v1,self.op,v2)
            self.conPoints[self.out].val = res

    def draw(self,surface,offset):
        pos = aoc.addPos(self.pos,offset)
        surface.blit(self.img,pos) 
        for conPoint in self.conPoints.values():
            conPoint.draw(surface,offset)
            
class Bit:
    def __init__(self,name,pos,conDir):
        self.val = -1
        self.pos = pos
        self.name = name
        
        pos = aoc.addPos(pos,(8,8))
        self.conPoint = ConnexionPoint(name,aoc.addPos(pos,aoc.sclPos(8,aoc.dirs4[conDir])))
        
    def setVal(self, val):
        self.val = val
        self.conPoint.val = val
        
    def update(self):
        if (self.conPoint.val != self.val):
            self.val = self.conPoint.val
        
    def getConPoint(self,name):
        return self.conPoint
    def draw(self,surface,offset):
        pos = aoc.addPos(self.pos,offset)
        surface.blit(valueImgs[self.val],pos) 
        self.conPoint.draw(surface,offset)

class Circuit:
    def __init__(self):
        self.allbits = []
        self.allgates = []
        self.alllines = []
        self.bits = {}
        self.offset = (0,0)
        
        
    def createHalfAdder(self,index):
        basePos = (32,32 + index * 144)
        baseStr = str(index).zfill(2)
        inX = Bit("x"+baseStr,aoc.addPos(basePos,(-24,32)),aoc.east)
        inY = Bit("y"+baseStr,aoc.addPos(basePos,(8,64)),aoc.east)
        inX.setVal(random.randint(0, 1))
        inY.setVal(random.randint(0, 1))
        outC = Bit("co"+baseStr,aoc.addPos(basePos,(128,128)),aoc.east)
        outZ = Bit("z"+baseStr,aoc.addPos(basePos,(328,48)),aoc.west)
        xor1 = Gate("XOR",inX.name,inY.name,outZ.name,aoc.addPos(basePos,(80,32)))
        and1 = Gate("AND",inX.name,inY.name,outC.name,aoc.addPos(basePos,(80,80)) )
        bits = [inX,inY,outC,outZ]
        gates = [xor1,and1]
        lines = []
        for bit in [inX,inY]:
            for gate in gates:
                conPoint = gate.getConPoint(bit.name)
                if conPoint != None:
                    lines.append(ConnexionLine(bit.getConPoint(bit.name),conPoint))
        for bit in [outC,outZ]:
            for gate in gates:
                conPoint = gate.getConPoint(bit.name)
                if conPoint != None:
                    lines.append(ConnexionLine(conPoint, bit.getConPoint(bit.name)))
        self.allbits.extend(bits)
        self.allgates.extend(gates)
        self.alllines.extend(lines)
  

    def createFullAdder(self,index):
        basePos = (32,32 + index * 144)
        baseStr = str(index).zfill(2)
        inX = Bit("x"+baseStr,aoc.addPos(basePos,(-24,32)),aoc.east)
        inY = Bit("y"+baseStr,aoc.addPos(basePos,(8,64)),aoc.east)
        inX.setVal(random.randint(0, 1))
        inY.setVal(random.randint(0, 1))      
        inC = Bit("ci"+baseStr,aoc.addPos(basePos,(128,0)),aoc.east)
        outC = Bit("co"+baseStr,aoc.addPos(basePos,(128,128)),aoc.east)
        outZ = Bit("z"+baseStr,aoc.addPos(basePos,(328,16)),aoc.west)
        
        tempxor = "xor_"+baseStr
        tempand1 = "and_tmp1_"+baseStr
        tempand2 = "and_tmp2_"+baseStr
        xor1 = Gate("XOR",inX.name,inY.name,tempxor,aoc.addPos(basePos,(80,32)))
        xor2 = Gate("XOR",inC.name,tempxor,outZ.name, aoc.addPos(basePos,(176,0)) )
        and1 = Gate("AND",inX.name,inY.name,tempand1, aoc.addPos(basePos,(80,80)) )
        and2 = Gate("AND",inC.name,tempxor,tempand2, aoc.addPos(basePos,(176,48)) )
        orgate = Gate("OR",tempand2,tempand1,outC.name, aoc.addPos(basePos,(240,64)) )
        bits = [inX,inY,inC,outC,outZ]
        gates = [xor1,xor2,and1,and2,orgate]
        lines = []
        for bit in [inX,inY,inC]:
            for gate in gates:
                conPoint = gate.getConPoint(bit.name)
                if conPoint != None:
                    lines.append(ConnexionLine(bit.getConPoint(bit.name),conPoint))
        for bit in [outC,outZ]:
            for gate in gates:
                conPoint = gate.getConPoint(bit.name)
                if conPoint != None:
                    lines.append(ConnexionLine(conPoint, bit.getConPoint(bit.name)))
        lines.append(ConnexionLine(xor1.getConPoint(tempxor), xor2.getConPoint(tempxor)))
        lines.append(ConnexionLine(xor1.getConPoint(tempxor), and2.getConPoint(tempxor)))
        lines.append(ConnexionLine(and2.getConPoint(tempand2), orgate.getConPoint(tempand2)))
        lines.append(ConnexionLine(and1.getConPoint(tempand1), orgate.getConPoint(tempand1)))
        self.allbits.extend(bits)
        self.allgates.extend(gates)
        self.alllines.extend(lines)
  
    def createCircuit(self,n):
        self.nbAdder = n
        self.createHalfAdder(0)
        for i in range(1,n):
            self.createFullAdder(i)
        for bit in self.allbits:
            self.bits[bit.name] = bit
    
    def draw(self,surface):
        firstUnsetCarry = -1
        for i in range(0,self.nbAdder):
            cout = "co" + str(i).zfill(2)
            bit = self.bits[cout]
            if firstUnsetCarry < 0 and bit.val == -1:
                firstUnsetCarry = bit.pos[1]
        if firstUnsetCarry + self.offset[1] > surface.get_height()-220:
            self.offset = aoc.subPos(self.offset, (0,1))


        surface.fill(backgroundColor)
        
        
        for i in range(self.nbAdder):
            h = (i+1) * 144 + 32 + self.offset[1]
            aoc.pygame.draw.line(surface,sepColor,(0,h),(surface.get_width(),h),width = 2)
       
        for line in self.alllines:
            line.draw(surface,self.offset)        
        for bit in self.allbits:
            bit.draw(surface,self.offset)
        for gate in self.allgates:
            gate.draw(surface,self.offset)

        surface.fill(headerColor,((0,0),(surface.get_width(),32)))
        aoc.pygame.draw.line(surface,sepColor,(32,0),(32,surface.get_height()),width = 2)
        aoc.pygame.draw.line(surface,sepColor,(64,0),(64,surface.get_height()),width = 2)
        aoc.pygame.draw.line(surface,sepColor,(352,0),(352,surface.get_height()),width = 2)
        surface.blit(coordImgs["X"],(8,8)) 
        surface.blit(coordImgs["Y"],(40,8)) 
        surface.blit(coordImgs["Z"],(360,8)) 

    def update(self):
        for line in self.alllines:
            line.update()
        for gate in self.allgates:
            gate.update()
        for bit in self.allbits:
            bit.update()
 
        for i in range(0,self.nbAdder):
            cin = "ci" + str(i+1).zfill(2)
            cout = "co" + str(i).zfill(2)
            if (cin in self.bits):
                self.bits[cin].setVal(self.bits[cout].val)
            
    
display = aoc.Display(True, 380, 800, 1 , 0)
circuit = Circuit()
circuit.createCircuit(45)
circuit.draw(display.surface)
circuit.update()
display.update()
display.waitKey()
display.waitKey()
while True:
    circuit.draw(display.surface)
    circuit.update()
    display.update()
    #time.sleep(0.05)
    


def addtNumbers(indexBit, val1 , val2):
    results = {}
    outputs= []
    for i in range(46):
        results["x"+str(i).zfill(2)] = 0 if i != indexBit else val1
        results["y"+str(i).zfill(2)] = 0 if i != indexBit else val2
        outputs.append("z"+str(45-i).zfill(2))
    outputValues = [eval(results,out) for out in outputs]
    binaryString = ''.join([str(i) for i in outputValues])
    number = int(binaryString, 2)
    checkNumber = (val1+val2)<<indexBit
    print("bit"+str(indexBit).zfill(2) , binaryString, "!!!!!!" if number != checkNumber else "")
    if number != checkNumber:
        return "z"+str(indexBit)
    else:
        return None



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

