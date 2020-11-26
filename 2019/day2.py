import copy 

initial_numbers= []
f = open('input_day2.txt','r')
for line in f:
    initial_numbers = line.split(",")


def test_combo(a,b):
    numbers = copy.copy(initial_numbers)

    i = 0
    opcode = int(numbers[0])
    print len(numbers)
    numbers[1] = a
    numbers[2] = b

    while opcode != 99 and (i+4) < len(numbers): 
        opcode = int(numbers[i])
        src_adr1 = int(numbers[i+1])
        src_adr2 = int(numbers[i+2])
        dst_adr  = int(numbers[i+3])
        n1 = int(numbers[src_adr1])
        n2 = int(numbers[src_adr2])
        i = i + 4
        if opcode == 1:
            n1 = int(numbers[src_adr1])
            numbers[dst_adr] =  n1 + n2
            # print ("Adr[{0}]({1}) = Adr[{2}]({3}) + Adr[{4}]({5})".format(dst_adr,numbers[dst_adr],src_adr1,n1,src_adr2,n2))
        elif opcode == 2:
            numbers[dst_adr] = n1 * n2
            # print ("Adr[{0}]({1}) = Adr[{2}]({3}) * Adr[{4}]({5})".format(dst_adr,numbers[dst_adr],src_adr1,n1,src_adr2,n2))
    
    print("Combo {0} gives {1}".format(a*100+b,numbers[0]))
    return numbers[0]

for a in range(99):
    for b in range (99): 
        val = int(test_combo(a,b))
        if val == 19690720:
            print("Winning Combo {0} gives {1}".format(a*100+b,val))
            quit() 