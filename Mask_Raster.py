###############################################################################
## Scipt:       Mask_Rasters.py
## Written By:  Everett Blakley
## Description: Takes input raster and masks it based on the ideal counties
##              as well as urban and water areas that need to be removed
###############################################################################

import arcpy

arcpy.CheckOutExtension("Spatial")

arcpy.env.snapRaster = r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\blank_raster.tif"
mask = r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\county_mask.tif"
arcpy.env.workspace = r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\Expected_Time\RF_Max\v1"
inputRasters = arcpy.ListRasters()
outputDir = r"C:\Users\evere\Documents\Grasshopper Research\Spatial_Files\Rasters\Expected_Time\RF_Max\v2"

for raster in inputRasters:
    outName = raster[: raster.find("v")] + "v2.tif"
    arcpy.gp.Times_sa(raster, mask, outputDir + "\\" + outName)
    print(raster)

arcpy.CheckInExtension("Spatial")
