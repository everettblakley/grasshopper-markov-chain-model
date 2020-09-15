import arcpy
from arcpy import env
from arcpy.sa import *
import numpy

env.workspace = r"E:\Grasshopper Research\IDW2"

bound = 10
rastList = arcpy.ListRasters()
YearList = range(1983, 2017)

RastArray = numpy.zeros((1073, 667, 34))
rows = RastArray.shape[0]
cols = RastArray.shape[1]
years = RastArray.shape[2]

##for k in range(0, years):
##    tempArray = arcpy.RasterToNumPyArray(rastList[k])
##    for i in range(0, rows):
##        for j in range(0, cols):
##            RastArray[i,j,k] = tempArray[i,j]
##    print str(rastList[k]) +" loaded into RastArray"

RastArray = numpy.load('RasterArray.npy')

stateArray = numpy.zeros((1073, 667, 33))
for i in range(0, 1073):
    for j in range(0, 667):
        for k in range(0, 33):
            if RastArray[i,j,k] <= bound and RastArray[i,j,k+1] <= bound:
                stateArray[i,j,k] = 0
            elif RastArray[i,j,k] <= bound and RastArray[i,j,k+1] > bound:
                stateArray[i,j,k] = 2
            elif RastArray[i,j,k] > bound and RastArray[i,j,k+1] <= bound:
                stateArray[i,j,k] = 1
            else:
                stateArray[i,j,k] = 3

numpy.save('stateArray', stateArray)
print "stateArray created"
stateSums = numpy.zeros((1073,667,2))

for u in range(0,1073):
    for v in range(0, 667):
        for w in range(0,33):
            if stateArray[u,v,w] == 0:
                stateSums[u,v,0] += 1
            elif stateArray[u,v,w] == 1:
                stateSums[u,v,0] += 1
            elif stateArray[u,v,w] == 2:
                stateSums[u,v,1] += 1
            else:
                stateSums[u,v,1] += 1

numpy.save('stateSums', stateSums)
print "stateSums computed"

transProb = numpy.zeros((1073,667,4))

for i in range(0, 1073):
    for j in range(0, 667):
        transProp = numpy.zeros((2,2))
        for k in range(0, 33):
            if stateArray[i,j,k] == 0:
                transProp[0,0]+=1
            elif stateArray[i,j,k] == 1:
                transProp[0,1] += 1
            elif stateArray[i,j,k] == 2:
                transProp[1,0] += 1
            else:
                transProp[1,1] += 1
        transProb[i,j,0] = transProp[0,0]/stateSums[i,j,0]
        transProb[i,j,1] = transProp[0,1]/stateSums[i,j,0]
        transProb[i,j,2] = transProp[1,0]/stateSums[i,j,1]
        transProb[i,j,3] = transProp[1,1]/stateSums[i,j,1]

numpy.save('TransitionProbabiliites', transProb)            



