
pattern = (0,1,0,-1)


def buildPatternTable(seq):
    seqLen = len(seq)
    for i in range(seqLen):
        nbRep = i +1 
        sizePattern = len(pattern) * nbRep
        for j in range(seqLen):
            index = ((j+1) % sizePattern) // nbRep
            pattern_table[ i * seqLen + j] = pattern[index]

def doPhasePart1(seq):
    resStr = ""
    seqLen = len(seq)
    for i in range(seqLen):
        val = 0
        nbRep = i +1 
        sizePattern = len(pattern) * nbRep     
        for j,c2 in enumerate(seq):
            index = ((j+1) % sizePattern) // nbRep
            val += int(c2) * pattern[index]
        val = int(abs(val)) % 10
        resStr += str(val)
    return resStr
   
f = open('input_day16.txt','r')
sequence = f.readline()
offset = int(sequence[0:7])
print(offset)

#part1
#buildPatternTable(sequence)
#for i in range(100):
    #sequence = doPhasePart1(sequence)
    #print(i+1, ' => ' , sequence)

seqlen = len(sequence)
seqmul = [0] * (seqlen*10000 - offset)
index = offset % seqlen
for i in range(offset,seqlen*10000):
    seqmul[i - offset] = int(sequence[index])
    index = index + 1 if index < (seqlen-1) else 0

def doPhasePart2(seq):
    seqLen = len(seq)
    val = 0
    for i in reversed(range(seqLen)):
       val = val + seq[i]
       cval = abs(val) % 10
       seq[i] = cval

# in part 2 we only care about characters after a given index
for i in range(100):
    doPhasePart2(seqmul)
    chars = seqmul[0:8]
    chars2 = [str(char) for char in chars]
    seqtext = ''.join(chars2)
    print(i+1, ' => ' , seqtext)




