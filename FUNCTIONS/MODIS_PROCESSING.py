# ===================================================================================== #
### Import Packages
import numpy as np
import pymodis
import fiona
from osgeo import gdal
import rasterio
import rasterio.mask

# ===================================================================================== #
### Class ConvertToGeoTiff
class ConvertToGeoTiff:

    ## Self destruction
    def __init__(self, hdfName, outNamePrefix, subset = [1, 0], res = None, outFormat = "GTiff", epsg = 4326):
        self.hdfName   = hdfName
        self.prefix    = outNamePrefix
        self.subset    = subset
        self.res       = res
        self.outFormat = outFormat
        self.epsg      = epsg
    
    ## Convert
    def Convert(self):
        mosaic = pymodis.convertmodis_gdal.convertModisGDAL(self.hdfName, self.prefix, self.subset, self.res, self.outFormat, self.epsg)
        mosaic.run(quiet = True)
        return None

# ===================================================================================== #
### Function Merge Two GeoTiff Files
def MergeTwoGeoTiff(tifList, outFolder):
    
    vrt = gdal.BuildVRT(outFolder + "merged.vrt", tifList)
    gdal.Translate(outFolder + "merged.tif", vrt)
    del vrt

    return None

# ===================================================================================== #
### Function Mask
def MaskGeoTiffWithShapefile(tifName, shapefile, outName):

    ## Read files
    with fiona.open(shapefile, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
    with rasterio.open(tifName) as src:
        outImage, outTransform = rasterio.mask.mask(src, shapes, crop = True)
        outMeta = src.meta

    ## Update metadata
    outMeta.update({"driver": "GTiff",
                "height": outImage.shape[1],
                "width": outImage.shape[2],
                "transform": outTransform})
    
    ## Write the Masked GeoTiff
    with rasterio.open(outName, "w", **outMeta) as dest:
        dest.write(outImage)
    
    return None

# ===================================================================================== #
### Class Eliminate No Data Value and Calculate Mean
class GeoTiffToArray:

    ## Self construction
    def __init__(self, tifFolder, tifName, band, scaleFactor = 0.1, maxValidValue = 30000):
        self.tifFolder     = tifFolder
        self.tifName       = tifName
        self.raster        = rasterio.open(self.tifFolder + "\\" + self.tifName)
        self.band          = band
        self.scaleFactor   = scaleFactor
        self.maxValidValue = maxValidValue

    ## Eliminate no data value and multiply the scale factor
    def Calculate(self):
        
        # Year and julian day
        year = self.tifName[:4]
        julianDay = self.tifName[4:7]

        # Value array
        value = self.raster.read(self.band)
        self.raster = None
        value = np.where(value <= self.maxValidValue, value * self.scaleFactor, np.nan)
        
        # Daily mean
        if int(year)%4 != 0 or int(year)%100 == 0:
            value = value / 5 if int(julianDay) == 361 else value / 8
        else:
            value = value / 6 if int(julianDay) == 361 else value / 8
        
        return value
    

    
    






