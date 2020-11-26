import copy 
import pygame
import itertools

width=25
height=6
imglength = width * height


f = open('input_day8.txt','r')
l = f.readline()

nblayer = int((len(l)-1) / imglength)
print(nblayer)
print(imglength)

layers = []
minNbZero = imglength
maxLayer = 0

for i in range(0,nblayer):
    layer = l[i*imglength:(i+1)*imglength]
    nbzero = layer.count('0')
    if (nbzero < minNbZero):
        minNbZero = nbzero
        maxLayer = i
        print("layer {0} has {1} 0 in it".format(i,nbzero))
        print(len(layer))
    
    layers.append(layer)

# 0 black
# 1 white
# 2 transparent
finalImg = []
for i in range(0,imglength):
    finalImg.append('2')

for layer in layers:
    for i in range(0,imglength):
        pix = int(layer[i])
        oldpix = int(finalImg[i])
        if (oldpix == 2):
            finalImg[i] = layer[i]

displayImg = "".join(finalImg)
displayImg = displayImg.replace('0',' ')
displayImg = displayImg.replace('1','#')

for h in range(0,height):
    print(displayImg[h*width:(h+1)*width])


#theLayer = layers[maxLayer]
#nbOne = theLayer.count('1')
#nbTwo = theLayer.count('2')
#print("layer {0} has {1} 1 n it".format(maxLayer,nbOne))
#print("layer {0} has {1} 2 n it".format(maxLayer,nbTwo))
#print(nbOne * nbTwo)



