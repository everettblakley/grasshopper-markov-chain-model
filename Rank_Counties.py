import arcpy
from arcpy import env
import numpy as np

env.workspace = r"E:\Grasshopper Research\Shapefiles\Points Clipped\Full"

countiesDict = np.load('counties.npy').item()
counties = r"E:\Grasshopper Research\Shapefiles\Counties_prj.shp"

fc = arcpy.ListFeatureClasses()
fc_new = []
for i in fc:
    j = i.strip('.shp')
    fc_new.append(j)
    

years = range(1983, 2017)

countSum = 0
avgCount = 0
with arcpy.da.UpdateCursor(counties, ["years", "AvgCount", "Comb2", "GEOCODE"]) as cursor:
    for row in cursor:
        if (row[0] <= 15) and (row[1] <= 25):
            row[2] = 1
        elif (row[0] <= 15) and (row[1] > 25 and row[1] <= 36):
            row[2] = 2
        elif (row[0] <= 15) and (row[1] > 36):
            row[2] = 3
        elif (row[0] > 15 and row[0] <= 30) and (row[1] <= 25):
            row[2] = 4
        elif (row[0] > 15 and row[0] <= 30) and (row[1] > 25 and row[1] <= 36):
            row[2] = 5
        elif (row[0] > 15 and row[0] <= 30) and (row[1] > 36):
            row[2] = 6
        elif (row[0] >30) and (row[1] <= 25):
            row[2] = 7
        elif (row[0] >30) and (row[1] > 25 and row[1] <= 36):
            row[2] = 8
        elif (row[0] >30) and (row[1] > 36):
            row[2] = 9
        else:
            row[2] = 0
        print countiesDict[row[3]], row[2]
        cursor.updateRow(row)
            
                


