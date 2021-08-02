# ===================================================================================== #
### Import Packages
from FUNCTIONS import MODIS_PROCESSING
import os
import sys

# ===================================================================================== #
### Data

## Folder
dataset = sys.argv[1]
folder  = "/work6/L.prcpltwfkwd/MODIS/" + dataset + "/"
h28v06List = [_ for _ in os.listdir(folder) if "h28v06" in _]
h29v06List = [_ for _ in os.listdir(folder) if "h29v06" in _]

## Shapefile
shapefile = "Taiwan.Main/Taiwan.Main.shp"

# ===================================================================================== #
### Main

## Folders
tmp = "/work6/L.prcpltwfkwd/MODIS/" + dataset + ".GeoTiff/tmp/"

## Loop
count = 0
for f28, f29 in zip(h28v06List, h29v06List):

    # Julian days
    julianDay = f28[9:16]

    # Convert hdf to GeoTiff
    class28 = MODIS_PROCESSING.ConvertToGeoTiff(folder + f28, tmp + "h28")
    class29 = MODIS_PROCESSING.ConvertToGeoTiff(folder + f29, tmp + "h29")
    class28.Convert()
    class29.Convert()

    # Merge two GeoTiff files
    tifList = [_ for _ in os.listdir(tmp) if "h2" in _]
    tifList[0] = tmp + tifList[0]
    tifList[1] = tmp + tifList[1]
    MODIS_PROCESSING.MergeTwoGeoTiff(tifList, tmp)

    # Mask
    tifName = tmp + "merged.tif"
    outName = "/work6/L.prcpltwfkwd/MODIS/" + dataset + ".GeoTiff/" + julianDay + ".tif"
    MODIS_PROCESSING.MaskGeoTiffWithShapefile(tifName, shapefile, outName)

    # Count
    if count%50 == 0:
        print(count)
    count += 1
    












