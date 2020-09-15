import json
import arcpy

dataPath = r"C:\Users\evere\Documents\personal-website\everett-blakley-com\src\data\grasshoppers\gh-all-point-data.json"

##data = json.load(open(dataPath))

shapefile = r"C:\Users\evere\Documents\Grasshopper Research\Shapefiles\Master_Point_data.shp"

fields = ["Shape", "FID", "Latitude", "Longitude", "County", "Date",
          "Year", "Month", "Day", "Road", "Field"]

for field in [field.name for field in arcpy.ListFields(shapefile)]:
    if field not in fields:
        arcpy.DeleteField_management(shapefile, field)
        print(field)
