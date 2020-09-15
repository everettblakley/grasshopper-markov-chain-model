###############################################################################
## Scipt:       Compute_IDW_Rasters.py
## Written By:  Everett Blakley
## Description: Script to create the IDW rasters for each year throughout the
##              province
###############################################################################

import arcpy
from arcpy import env
from arcpy.sa import *

## Set-up Environment Settings for Geoprocessing
env.overwriteOutput = True
env.snapRaster = r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\blank_raster.tif"
env.cellSize = env.snapRaster
roadOutput = (
    r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\IDW\Road\v1"
)
fieldOutput = (
    r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\IDW\Field\v1"
)
rfMaxOutput = (
    r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\IDW\RX_Max\v1"
)

arcpy.CheckOutExtension("Spatial")

## Declare variables for use in the IDW creation
Points = r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Master_Point_data.shp"
YearList = range(1983, 2017)

##For loop to create a series of 34 IDW based on the point file Master_10TM.shp
for year in YearList:
    yr_layer = "IDW_" + str(year)  ##Variable to serve as the output name for the IDW
    query = '"Year" = {0}'.format(year)
    arcpy.MakeFeatureLayer_management(
        Points, yr_layer, query
    )  ##Temporary point file for current year
    roadIDW = Idw(
        yr_layer, "Road", env.cellSize
    )  ##IDW created based on the Road counts for the current year
    roadIDW.save(roadOutput + "/IDW_road_{0}_v1.tif".format(year))  ##Save the IDW
    fieldIDW = Idw(
        yr_layer, "Field", env.cellSize
    )  ##IDW created based on the Road counts for the current year
    fieldIDW.save(fieldOutput + "/IDW_field_{0}_v1.tif".format(year))  ##Save the IDW
    maxIDW = Idw(
        yr_layer, "MAX_RF", env.cellSize
    )  ##IDW created based on the Road counts for the current year
    maxIDW.save(rfMaxOutput + "/IDW_RF_Max_{0}_v1.tif".format(year))  ##Save the IDW
    print("Completed {0}".format(year))

