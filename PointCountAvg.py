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
with arcpy.da.UpdateCursor(counties, ["GEOCODE", "AvgCount"]) as cursor:
    for row in cursor:
        if row[0] in fc_new:
            for year in years:
                temp = arcpy.MakeFeatureLayer_management(str(row[0])+'.shp',
                                                         str(row[0])+"_"+str(year),
                                                         '"Year" = ' + str(year))
                count = arcpy.GetCount_management(temp)
                count = str(count).strip("'")
                countSum += int(count)
        avgCount = countSum/34
        row[1] = avgCount
        print countiesDict[row[0]], countSum, avgCount
        countSum = 0
        cursor.updateRow(row)
            
                


