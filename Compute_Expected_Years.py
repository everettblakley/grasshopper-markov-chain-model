###############################################################################
## Scipt:       Compute_Expected_Years.py
## Written By:  Everett Blakley
## Description: Compute the expected time the population will stay in each 
##              state before transitioning to a different state
###############################################################################

import arcpy
from arcpy import env
import numpy as np

env.workspace = r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\Expected_Time\RF_Max\v1"
env.overwriteOutput = True

## Load the transition probabilities
p01 = arcpy.RasterToNumPyArray(r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\Transition_Probability\RF_Max\v1\TransProb_p01_RF_Max_v1.tif")
p10 = arcpy.RasterToNumPyArray(r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\Transition_Probability\RF_Max\v1\TransProb_p10_RF_Max_v1.tif")

## Create empty arrays to store the expected times
exp0 = np.zeros((1073, 667))
exp1 = np.zeros((1073,667))
v0 = np.zeros((1073, 667))
v1 = np.zeros((1073, 667))
for i in range(0, p01.shape[0]):
    for j in range(0, p01.shape[1]):
        a = p01.item((i,j))
        b = p10.item((i,j))
        if a > 0:
            exp0[i,j] = (1-a)/a
            v0[i,j] = (1-a)/(a*a)
        else:
            exp0[i,j] = 100
            v0[i,j] = 100*100
        if b > 0:
            exp1[i,j] = (1-b)/b
            v1[i,j] = (1-b)/(b*b)
        else:
            exp1[i,j] = 0
            v1[i,j] = 0
print("Expected Times and Variances computed")

## Save arrays as rasters
lowerLeft = arcpy.Point(185876.8675, 5426706.1087)
exp0_rast = arcpy.NumPyArrayToRaster(exp0, lowerLeft, 1000, 1000)
exp1_rast = arcpy.NumPyArrayToRaster(exp1, lowerLeft, 1000, 1000)
exp0_rast.save(env.workspace + r"\ExpTime_Uninf_RF_Max_v1.tif")
exp1_rast.save(env.workspace + r"\ExpTime_Inf_RF_Max_v1.tif")
print "Expected Time rasters saved"
v0_rast = arcpy.NumPyArrayToRaster(v0, lowerLeft, 1000, 1000)
v1_rast = arcpy.NumPyArrayToRaster(v1, lowerLeft, 1000, 1000)
v0_rast.save(env.workspace + r"\ExpVar_Uninf_RF_Max_v1.tif")
v1_rast.save(env.workspace + r"\ExpVar_Inf_RF_Max_v1.tif")
print "Variance rasters saved"