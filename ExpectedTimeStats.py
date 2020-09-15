import arcpy
from arcpy import env
import numpy as np

env.workspace = r"E:\Grasshopper Research\Markov Model\Split1"

list = arcpy.ListRasters("*et*")

print "Raster, Total, 1 - 5, 5 - 10, 10 - 20, 20 - 30, 30 - 100"

for rast in list:
    count0 = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    array = arcpy.RasterToNumPyArray(rast)
    for i in range(0, array.shape[0]):
        for j in range(0, array.shape[1]):
            if array.item((i,j)) <= 5:
                count0 += 1
            elif array.item((i,j)) > 5 and array.item((i,j)) <= 10:
                count1 += 1
            elif array.item((i,j)) > 10 and array.item((i,j)) <= 20:
                count2 += 1
            elif array.item((i,j)) > 20 and array.item((i,j)) <= 30:
                count3 += 1
            else:
                count4 += 1
    temp = [str(rast), int(count0+count1+count2+count3+count4), int(count0), int(count1), int(count2), int(count3), int(count4)]
    print temp
    
