#최상위디렉터리에서 수행되어야함
import pandas as pd
import geopandas as gpd
import numpy as np
import scipy.spatial as sp
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import os
import glob
#import concurrent.futures
#import gc
#from multiprocessing import freeze_support
d,gdf=None,None
def analysis(name):
    df=pd.read_csv(str(name))
    print(df)
    df=df[df['x']<39]
    ax=gdf.plot()#show mountain graphices
    print(df)
    points=gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df.y,df.x),crs='epsg:4326')
    #RAW data Scatterplot
    ax.scatter(points['y'],points['x'],c='red')
    joined_points=gpd.sjoin(points,gdf)
    joined_points=points
    df_joined_points=pd.DataFrame()
    df_joined_points['x']=joined_points['y']
    df_joined_points['y']=joined_points['x']
    #show Joined Scatter plot
    ax.scatter(df_joined_points['x'],df_joined_points['y'])
    print(df_joined_points)
    #create model and prediction
    dbs=DBSCAN(eps=d,min_samples=3).fit(df_joined_points[['x','y']]).labels_   
    df_joined_points=df_joined_points.assign(cluID=dbs)
    for i in range(len(dbs)):        
        data=df_joined_points.loc[df_joined_points.cluID==i]
        print(data)
        #ax.scatter(data['x'],data['y'])
        data=data.drop('cluID',axis=1)
        if len(data)>2:  
            data_=np.array(data)
            print(data_)
            hull=sp.ConvexHull(data_)
            for simplex in hull.simplices:
                print(simplex)
                ax.plot(data_[simplex, 0], data_[simplex, 1], 'k-')
    plt.show()                    
    plt.savefig(str(name[:-3])+str('png'))
    ax.savefig(str(name[:-3])+str('png'))
def main():
    global d,gdf
    d=0.018
    gdf=gpd.read_file('data/korea_forest_map.shp').to_crs('epsg:4326')

    #for expriment
    file='data/kml_csv_kor_only/2022_4_10-15_J1_VIIRS_C2_result_korea.csv'
    analysis(file)

    #for all files in the directory(single Core)
    #for file in glob.glob('data/kml_csv_kor_only/*.csv'):
    #    analysis(file)

    #for all files in the directory(multi Core)
    #if(os.path.isdir('data/geojson/UTMK/')==False):
    #    os.makedirs('data/geojson/UTMK/')  
    #with concurrent.futures.ProcessPoolExecutor() as executor:
    #    imported_files = glob.glob('data/geojson/WGS84/*.geojson')
    #    executor.map(EPSGcvter, imported_files)
