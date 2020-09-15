import arcpy
from arcpy import env
import numpy as np

env.workspace = r"E:\Grasshopper Research\IDW_Full\IDW_Clipped"
counties = np.load('counties.npy').item()
folders = ["p00", "p01", "p10", "p11"]

for folder in folders:
    env.workspace = r"E:\Grasshopper Research\IDW_Full\IDW_Clipped" + "/" + str(folder)
    globals()['rastList_%s' % folder] = arcpy.ListRasters()

print "STD DEV TRANSITION PROBABILITIES BY COUNTY"
print "Geocode, County Name, p00, p01, p10, p11"
for i in range(0, len(rastList_p00)):
    rast = rastList_p00[i]
    for folder in folders:
        env.workspace = r"E:\Grasshopper Research\IDW_Full\IDW_Clipped" + "\\" + str(folder)
        name = str(rast[0:4])+"_"+str(folder)+".tif"
        globals()['std_%s' % folder] = arcpy.GetRasterProperties_management(name, "STD")
    
    print '="'+ str(rast[0:4]) +'"'+ "," + str(counties[rast[0:4]]) + ", " + str(std_p00) \
          + ", " + str(std_p01)+", "+str(std_p10)+", "+str(std_p11)






    

