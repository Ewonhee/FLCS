import geopandas as gpd
import matplotlib.pyplot as plt
import glob
import pandas as pd
shapefiles=glob.glob("C:/Users/SON/FLCS-1/data/shp_type2/asset/*.shp")

gdf = pd.concat([gpd.read_file(shp)for shp in shapefiles]).pipe(gpd.GeoDataFrame)
gdf.crs={'init':'epsg:4326'}
gdf.to_file("GEOproc/result.shp")
#gdf.plot(aspect=1)
#plt.show()

#/home/sons/FLCS/GEOproc