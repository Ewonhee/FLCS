#최상위디렉터리에서 수행되어야함
import pandas as pd
import geopandas as gpd
import numpy as np
import scipy.spatial as sp
from sklearn.cluster import DBSCAN
import os
import glob
import concurrent.futures
import gc
def EPSGcvter(name):
    jsons=gpd.read_file(name)
    jsons=jsons.to_crs('epsg:5179')
    jsons.to_file('data/geojson/UTMK/'+str(name.split('/')[3].split('.')[0])+'UTMK.geojson', driver='GeoJSON')
def analysis(name):
    df=pd.read_csv(str(name))
    df=df[df['x']<39]
    points=gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df.y,df.x),crs='epsg:4326')
    joined_points=gpd.sjoin(points,gdf)
    df_joined_points=pd.DataFrame()
    df_joined_points['x']=joined_points['y']
    df_joined_points['y']=joined_points['x']
    # create model and prediction
    try:
        dbs=DBSCAN(eps=d,min_samples=3).fit(df_joined_points[['x','y']]).labels_
        df_joined_points=df_joined_points.assign(cluID=dbs)
    except:
        print(str(name)+"DBSCAN오류: smaple이 minsamples보다 작습니다.")
        return
    dbs=DBSCAN(eps=d,min_samples=3).fit(df_joined_points[['x','y']]).labels_        
    df_joined_points=df_joined_points.assign(cluID=dbs)
    exportJSON=''
    for i in range(len(dbs)):
            data=df_joined_points.loc[df_joined_points.cluID==i]
            data=data.drop('cluID',axis=1)
            if len(data)>2:  
                data_=np.array(data)
                hull=sp.ConvexHull(data_)
                cnt=1
                exportJSON=exportJSON+'['
                for i in hull.vertices:
                    exportJSON=exportJSON+str('['+str(hull.points[i,0])+','+str(hull.points[i,1])+'],')
                    if(cnt<len(hull.vertices)):
                        cnt=cnt+1
                    else:
                        exportJSON=exportJSON+str('['+str(hull.points[hull.vertices[0],0])+','+str(hull.points[hull.vertices[0],1])+']],')
    out='{"type": "MultiPolygon","coordinates": [['+exportJSON[:-1]+']]}'
    addr=str('data/geojson/WGS84/'+str(name.split('/')[2][:-4])+'.geojson')
    f=open(addr,'w')
    f.write(out)
    f.close()
    gc.collect(generation=2)       
d=0.10
gdf=gpd.read_file('data/korea_forest_map.shp').to_crs('epsg:4326')
if(os.path.isdir('data/geojson/WGS84/')==False):
    os.makedirs('data/geojson/WGS84/')  
with concurrent.futures.ProcessPoolExecutor() as executor:
    imported_files = glob.glob("data/kml_csv_kor_only/*.csv")
    executor.map(analysis, imported_files)
if(os.path.isdir('data/geojson/UTMK/')==False):
    os.makedirs('data/geojson/UTMK/')  
with concurrent.futures.ProcessPoolExecutor() as executor:
    imported_files = glob.glob('data/geojson/WGS84/*.geojson')
    executor.map(EPSGcvter, imported_files)
