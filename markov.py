import arcpy
from arcpy import env
from arcpy.sa import *

env.workspace = r"E:\Grasshopper Research\Shapefiles"
env.overwriteOutput = True
env.snapRaster = r"E:\Grasshopper Research\Shapefiles\Alberta_rast2"

arcpy.CheckOutExtension("Spatial")

Taber = "e://Grasshopper Research/Shapefiles/Points Clipped/Taber_pts.shp"
Taber_Shp = r"E:\Grasshopper Research\Shapefiles\GDB Files\Taber_10TM.shp"
Output_Loc = "e://Grasshopper research/output/"
cell_size = arcpy.GetRasterProperties_management("Alberta_rast2", "CELLSIZEX")
taber_field = arcpy.ListFields(Taber)

cursor = arcpy.da.SearchCursor(Taber, ["Latitude", "Longitude","Year", "Road"])
YearList = [1986,1987,1988]
iter = 0
year = 1986
for row in cursor:
    if row[2] not in YearList:
        YearList.append(row[2])

##    for year in YearList:
##        if row[2]==year:
##            iter += 1
##        print "The number of row in " +str(year)+" is " +str(iter)
##        iter =0
        
##for year in YearList:
##    arcpy.env.extent = Taber_Shp
##    yr_layer = "TaberIDW_100m" + str(year)
##    arcpy.MakeFeatureLayer_management(Taber, yr_layer, '"YEAR"='+str(year))
##    outidw = Idw(yr_layer, "Road", 1000)
##    outidw.save(Output_Loc + str(yr_layer) +".tif")
##    print "IDW Raster created for " +str(year)

desc = arcpy.Describe(Taber_Shp)

xmin = desc.extent.XMin
xmax = desc.extent.XMax
ymin = desc.extent.YMin
ymax = desc.extent.YMax

extent = [xmin, xmax, ymin, ymax]
print extent
yr_layer = "TaberIDW_" + str(year)
arcpy.MakeFeatureLayer_management(Taber, yr_layer, '"YEAR"='+str(year))
outidw = Idw(yr_layer, "Road", cell_size)
##outidw.save(Output_Loc + str(yr_layer) +".tif")
idw_clip = arcpy.Clip_management(outidw, extent, yr_layer +"_clip.tif", "","", True, "")
print "Clipped IDW Raster created for " +str(year)


del year
##del row
##del cursor
