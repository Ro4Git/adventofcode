

# max length 119315717514047
numiteration  = 101741582076661
#numiteration = 1

deck = []
maxlength = 119315717514047
fa = 1
fb = 0
# new pos = pos * a + b


#for i in range(maxlength):
#    deck.append(i)

def doNewStack(doOp):
    if (doOp):
        doOperation(-1,-1)
    #deck.reverse()
    return deck

def doCut(n,doOp):
    if (doOp):
        doOperation(1,-n)
    #newdeck = deck[n:] + deck[:n]
    #return newdeck
    return deck

def doDealInc(n,doOp):
    if (doOp):
        doOperation(n,0)
    #pos = 0
    #newdeck = [0] * len(deck)
    #for c in deck:
    #    newdeck[pos] = c
    #    pos += n
    #    pos = pos % len(deck)
    #return newdeck
    return deck

def newPos(n):
    return (fa * n + fb) % maxlength

def modinv(a, m):
    return pow(int(a), int(m-2), int(m))

def oldPos(n):
    inv = modinv(fa,maxlength)
    return ((n + maxlength- fb) * inv) % maxlength

def doOperation(a,b):
    global fa
    global fb
    fa = (a * fa) % maxlength
    fb = (fb*a + b) % maxlength

def sumPov(a,n):
    num = int(pow(a,n+1,maxlength)) - 1
    den = modinv(a - 1, maxlength)
    return (num * den) % maxlength


f = open('input_day22.txt','r')

lines = f.readlines()

initFaFb = True 
for line in lines:
    if (line.find("deal into new stack") >= 0):
        deck = doNewStack(initFaFb)
    elif line.find("cut") >= 0:
        nStr = line[4:]
        deck =doCut(int(nStr),initFaFb)
    else:
        nStr = line[len("deal with increment")+1:]
        deck = doDealInc(int(nStr),initFaFb)

initFaFb = False

fb = (sumPov(fa,numiteration-1) * fb) % maxlength 
fa = pow(fa,numiteration, maxlength)


print("---------")
print(newPos(2019))
print(oldPos(3074))
print(oldPos(2020))



