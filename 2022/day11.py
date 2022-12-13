#Advent of code 2022: Day 11
#https://adventofcode.com/2022/day/11
import re, time, copy


class Monkey:
    def __init__(self,items=[],addOp = 0,mulOP = 1,divideTest = 1,destIfTrue = 0,destIfFalse = 0):
        self.items = items
        self.toAdd = addOp
        self.toMul = mulOP 
        self.divideTest = divideTest
        self.destIfTrue = destIfTrue
        self.destIfFalse = destIfFalse
        self.nbInspectedItems = 0
        self.globalModulo = 0

    def inspectItemPart1(self):
        self.nbInspectedItems += 1
        worry = self.items.pop(0)
        worry += self.toAdd 
        if self.toMul != None:
            worry *= self.toMul
        else:
            worry *= worry
        worry //= 3
        if (worry % self.divideTest == 0):
            return (worry,self.destIfTrue)
        else:
            return (worry,self.destIfFalse) 

    def inspectItemPart2(self):
        self.nbInspectedItems += 1
        worry = self.items.pop(0)
        worry += self.toAdd 
        if self.toMul != None:
            worry *= self.toMul
        else:
            worry *= worry
        worry = worry % self.globalModulo
        if (worry % self.divideTest == 0):
            return (worry,self.destIfTrue)
        else:
            return (worry,self.destIfFalse) 


    def inspectItemsPart1(self):
        moves = []
        for i in range(len(self.items)):
            moves.append(self.inspectItemPart1())
        return moves

    def inspectItemsPart2(self):
        moves = []
        for i in range(len(self.items)):
            moves.append(self.inspectItemPart2())
        return moves
    
    def appendItem(self,item):
        self.items.append(item)


f = open('input_day11.txt', 'r')
lines = f.readlines()
lines = [line.rstrip("\n") for line in lines]
f.close()

def readMonkey(monkeyLines):
    #Monkey 4:
    #  Starting items: 66, 90, 59, 90, 87, 63, 53, 88
    #  Operation: new = old + 7
    #  Test: divisible by 5
    #    If true: throw to monkey 1
    #    If false: throw to monkey 0
    items = re.findall(r"\d+",monkeyLines[1])
    items = [int(item) for item in items] 
    numOp = re.findall(r"\d+",monkeyLines[2])
    addOp = 0
    mulOp = 1
    if len(numOp):
        op = int(numOp[0])
        if monkeyLines[2][23] == "+":
            addOp = op
        else: 
            mulOp = op
    else:
        mulOp = None
    testDivisible = int(re.findall(r"\d+",monkeyLines[3])[0])
    destIfTrue = int(re.findall(r"\d+",monkeyLines[4])[0])
    destIfFalse = int(re.findall(r"\d+",monkeyLines[5])[0])
    return Monkey(items,addOp,mulOp,testDivisible,destIfTrue,destIfFalse)


def part1():
    Monkeys = []
    for i in range(8):
        Monkeys.append(readMonkey(lines[i*7:]))

    for i in range(20): 
        for monkey in Monkeys:
            moves = monkey.inspectItemsPart1()
            for m in moves:
                Monkeys[m[1]].appendItem(m[0])

    inspecteds = [m.nbInspectedItems for m in Monkeys]
    inspecteds.sort()
    businesslevel = inspecteds[-1]*inspecteds[-2]
    print(businesslevel)
    return 

def part2():
    Monkeys = []
    globalModulo = 1
    for i in range(8):
        monkey = readMonkey(lines[i*7:])
        Monkeys.append(monkey)
        globalModulo *= monkey.divideTest
    for i in range(8):
        Monkeys[i].globalModulo = globalModulo

    for i in range(10000): 
        for monkey in Monkeys:
            moves = monkey.inspectItemsPart2()
            for m in moves:
                Monkeys[m[1]].appendItem(m[0])

    inspecteds = [m.nbInspectedItems for m in Monkeys]
    inspecteds.sort()
    businesslevel = inspecteds[-1]*inspecteds[-2]
    print(businesslevel)


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