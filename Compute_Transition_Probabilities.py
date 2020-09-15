###############################################################################
## Scipt:       Compute_Transition_Probabilities.py
## Written By:  Everett Blakley
## Description: Script to compute the transition probabilities for grasshopper
##              populations as they transition from uninfested to infested
##              based on the Markov Chain principle
###############################################################################

import arcpy
from arcpy import env
from arcpy.sa import *
import numpy

## Bound between uninfested and infested
env.workspace = r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\IDW\RF_Max\v1"
env.overwriteOutput = True
bound = 9.67
rastList = arcpy.ListRasters()
YearList = range(1983, 2017)

## Create an empty 3D array to store all the population values in
## The raster template is 1073x667, and there are 34 years in the study
RastArray = numpy.zeros((1073, 667, 34))
rows = RastArray.shape[0]
cols = RastArray.shape[1]
years = RastArray.shape[2]

## Iterate through all the IDW rasters, convert each raster to a numpy array
## and load the cell values into the empty 3D array
for k in range(0, years):
    tempArray = arcpy.RasterToNumPyArray(rastList[k])
    for i in range(0, rows):
        for j in range(0, cols):
            RastArray[i,j,k] = tempArray[i,j]
    
print "Population array created"

## Create an empty 3D array to store the transition states at each transition
## point. If there are N years, then N-1 transition will occurs, hence 33 years
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

print "State Transition array created"

## Sum the number of times the model transitioned to a different state in 
## each cell
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
print "State Sums computed"

## Finally, for each cell, divide the number of times the population
## transitioned between states by the 
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
        if stateSums[i,j,0] != 0:
            transProb[i,j,0] = transProp[0,0]/stateSums[i,j,0]
            transProb[i,j,1] = transProp[0,1]/stateSums[i,j,0]
        else:
            transProb[i,j,0] = 0
            transProb[i,j,1] = 0
        if stateSums[i,j,1] != 0:
            transProb[i,j,2] = transProp[1,0]/stateSums[i,j,1]
            transProb[i,j,3] = transProp[1,1]/stateSums[i,j,1]
        else:
            transProb[i,j,2] = 0
            transProb[i,j,3] = 0
print "Transition Probabilities Computed"

## Save the arrays are rasters
outputDir = r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\Transition_Probability\RF_Max\v1"
lowerLeft = arcpy.Point(185876.8675, 5426706.1087)
for i in range(4):
    tempRast = arcpy.NumPyArrayToRaster(transProb[:,:,i], lowerLeft, 1000, 1000, "")
    tempRast.save(outputDir + r"\TransProb_p{0}{1}_RF_Max_v1.tif".format(0 if i < 2 else 1, i%2))
print "Tranistion probability rasters created"


