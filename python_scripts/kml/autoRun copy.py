#KML파일분석기 
#출력은 x,y로 구분되는 csv파일
#최상위디렉터리에서 수행되어야함
#데이터와 동일위치에 있어야함
import os
import glob
import concurrent.futures
from multiprocessing import freeze_support
import gc
from bs4 import BeautifulSoup as bs
import pandas as pd
import geopandas as gpd
import numpy as np
import scipy.spatial as sp
from sklearn.cluster import DBSCAN
#######################################
# P  A  N  E  L #
mode=False
d,gdf=0.10,None
base="test"   #[test, data]
mp=False      #멀티프로세싱 사용여부
#######################################

#_______________________________________________________________________________  
def CSV_cvtr(file):
    if os.path.isfile(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'.csv')==False:
        df=pd.DataFrame()
        fr = open(str(file), 'r') 
        lines =fr.read() 
        fr.close()
        xmls=bs(lines, 'html.parser')
        cords=xmls.findAll('coordinates')
        for cord in cords:
            cord.string=cord.string.lstrip('<coordinates>').rstrip('</coordinates>')
            coord=cord.string.split(',')
            df = df.append({'y':coord[0].strip(),'x':coord[1].strip()}, ignore_index=True)########################FW발생
            df.to_csv(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'.csv', index=False)
    else:
        print(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'.csv already exists')  
    if os.path.isfile(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'result_korea.csv')==False:
        df=pd.read_csv(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'.csv')
        res=df[(df["x"]>33.0640)&(df["x"]<43.0039)&(df["y"]>124.1100)&(df["y"]<131.5242)]
        res=res[["x","y"]]
        res.to_csv(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'result_korea.csv',index=False)
        print(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+"result_korea.csv Successfully Processed")
    else:
        print(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+"result_korea.csv Already Exist")
#_______________________________________________________________________________  
def GeoJSON_cvtr(name):
    gdf=gpd.read_file('data/korea_forest_map.shp').to_crs('epsg:4326')
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
    #결과물 플롯 증거로 저장할것
    #JSON모듈활용해 개량할것(0509)
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
    addr=str(base+'/geojson/WGS84/'+str(name.split('/')[1].split('\\')[1][:-4])+'.geojson')
    f=open(addr,'w')
    f.write(out)
    f.close()
    gc.collect(generation=2)
#_______________________________________________________________________________  
def EPSG_cvtr(name):
    jsons=gpd.read_file(name)
    jsons=jsons.to_crs('epsg:5179')
    jsons.to_file(base+'/geojson/UTMK/'+str(name.split('/')[3].split('.')[0])+'UTMK.geojson', driver='GeoJSON')
#_______________________________________________________________________________    

#######################################
if mp == True:
    if __name__=='__main__':
        freeze_support()
        #kml을 한국좌표 추출해 csv변환
        #data/kml/*.kml -> data/kml_csv_kor_only/*.csv
        with concurrent.futures.ProcessPoolExecutor() as executor:
            imported_files = glob.glob(base+"/kml/*.kml")
            executor.map(CSV_cvtr, imported_files)    
        #데이터 필터링 처리해서 WGS84좌표로 GeoJSON 변환
        #data/kml_csv_kor_only/*.csv -> data/geojson/WGS84/*.geojson
        with concurrent.futures.ProcessPoolExecutor() as executor:
            imported_files = glob.glob(base+"/kml_csv_kor_only/*.csv")
            executor.map(GeoJSON_cvtr, imported_files)
        #GeoJSON을 UTMK좌표로 변환
        #data/geojson/WGS84/*.geojson -> data/geojson/UTMK/*.geojson
        with concurrent.futures.ProcessPoolExecutor() as executor:
            imported_files = glob.glob(base+'/geojson/WGS84/*.geojson')
            executor.map(EPSG_cvtr, imported_files)
else:            
        imported_files = glob.glob(base+"/kml/*.kml")
        for file in imported_files:
            CSV_cvtr(file)
        imported_files = glob.glob(base+"/kml_csv_kor_only/*.csv")
        for file in imported_files:
            GeoJSON_cvtr(file)
        imported_files = glob.glob(base+'/geojson/WGS84/*.geojson')
        for file in imported_files:
            EPSG_cvtr(file)    
#######################################            