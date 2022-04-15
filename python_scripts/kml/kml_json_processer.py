
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import scipy.spatial as sp
from sklearn.cluster import DBSCAN
import numpy as np
d=0.10
exportJSON=''
# 열점데이터 읽고 북위로 필터링
df=pd.read_csv('data/kml_csv_kor_only/2022_4_12-12_SUOMI_VIIRS_C2result_korea.csv')
df=df[df['x']<39]
gdf=gpd.read_file('data/result.shp').to_crs('epsg:4326')
points=gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df.y,df.x),crs='epsg:4326')
joined_points=gpd.sjoin(points,gdf)
df_joined_points=pd.DataFrame()
df_joined_points['x']=joined_points['y']
df_joined_points['y']=joined_points['x']
fig=plt.figure(figsize=(30,10))
ax1=plt.subplot(1,3,1)
ax1.set_title('Original Data')
gdf.plot(ax=ax1)
points.plot(ax=ax1,color='red')
ax2=fig.add_subplot(1,3,2)
ax2.set_title('Data joined with forest form map')
gdf.plot(ax=ax2)
plt.scatter(df_joined_points['x'],df_joined_points['y'],color='red')
# create model and prediction
dbs=DBSCAN(eps=d,min_samples=3).fit(df_joined_points[['x','y']]).labels_
df_joined_points=df_joined_points.assign(cluID=dbs)
ax3=fig.add_subplot(1,3,3)
gdf.plot(ax=ax3)
ax3.set_title('Filtered & Clustered Data')
for i in range(len(dbs)):
    data=df_joined_points.loc[df_joined_points.cluID==i]
    data=data.drop('cluID',axis=1)
    if len(data)>2:  
        plt.scatter(data['x'],data['y'])
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
        for simplex in hull.simplices:
                plt.plot(data_[simplex, 0], data_[simplex, 1], 'k-')
out='{"type": "MultiPolygon","coordinates": [['+exportJSON[:-1]+']]}'     
f=open('data/result.json','w')
f.write(out)
f.close()
plt.show()