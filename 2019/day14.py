
coef_buffer = [0] * 1000 * 1000

def buildPhase(seq):
    seqLen = len(seq)
    for i in range(seqLen):
        
        for c2 in seq:

    seq[]


def doPhase(seq):
    seqLen = len(seq)
    for i in range(seqLen):

        for c2 in seq:

    seq[]



f = open('input_day16.txt','r')
sequence = f.readline()
    equation = line.split('=>')
    #right side
    costNode = extractCostNode(equation[1])
    recette = recipe(costNode[1])
    #left side
    leftside = equation[0].split(', ')
    for value in leftside:
        recette.addArc(extractCostNode(value))
    graph[costNode[0]] = recette

graph['ORE'] = recipe(1)

# part 1 
fuelNode = graph['FUEL']
fuelNode.evalGraph(1)
targetORE = graph['ORE'].nbrequired
print("Cost in ORE for 1 Fuel : ",targetORE)

# part 2 
costInORE = 0
targetORE = 1000000000000
nbFuelMax = 1000000000000
nbFuelMin = 0 

while nbFuelMin < nbFuelMax-1:
    targetFuel = (nbFuelMax + nbFuelMin) // 2
    fuelNode = graph['FUEL']
    fuelNode.resetGraph()
    fuelNode.evalGraph(targetFuel)
    costInORE = graph['ORE'].nbrequired
    print("Trying producting ",targetFuel," cost ", costInORE)
    if (costInORE < targetORE):
        # could have produced more fuel, increase target
        nbFuelMin = targetFuel
    else:
       # cost too high , decrease target
       nbFuelMax = targetFuel

print("Trying producting ",targetFuel," cost ", costInORE)


