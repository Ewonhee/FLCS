#시스템, 구동관련
import os
import glob
import concurrent.futures
from multiprocessing import freeze_support
import gc
#분석관련
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import scipy.spatial as sp
from sklearn.cluster import DBSCAN
import json
import matplotlib.pyplot as plt
#GIS관련
import geopandas as gpd
import getFcst
from shapely.geometry import Polygon
#SQL
import pymysql

#KML파일분석기 
#최상위디렉터리에서 수행되어야함
#######################################
# T  O  D  O   L  I  S  T #
    #릴리즈
# N  O  T  E   L  I  S  T #    
    #GeoJSON_cvtr: concurrnt.futures로 병렬처리 오류발생(원인 파악 불가, 실사용시 문제 없음)
#######################################
# P  A  N  E  L #
d=0.1                                                                                           #d-value
base="data"                                                                                    #베이스 폴더 지정[test, data]
mp=True                                                                                       #멀티프로세싱 사용여부
fig_evidence=False                                                                         #증거용플롯저장
db_host='localhost'                                                                        #DB호스트
db_user='root'                                                                                #DB유저
db_pw=''                                                                                 #DBPW
db_name='flcsdb'                                                                            #DB명
TBLname='crdnttable'                                                                    #테이블명
gdfloc='data/korea_forest_map.shp'                                               #셰이프파일 위치
conn,curs,insert_time=None,None,None                                        #DB용 전역변수 (시험용도외 건들지말것
SQLinsertMode=False
#######################################
def Dup_pass(file):
    if os.path.isfile(file):
        return True
    else:
        return False
#_______________________________________________________________________________  
def CSV_cvtr(file):
    if Dup_pass(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'.csv')==False:
        fr = open(str(file), 'r') 
        lines =fr.read() 
        fr.close()
        xmls=bs(lines, 'html.parser')
        cords=xmls.findAll('coordinates')
        fr = open(str(file), 'r') 
        lines =fr.read() 
        fr.close()
        xmls=bs(lines, 'html.parser')
        cords=xmls.findAll('coordinates')
        cd=list(map(lambda x:x.string.split(','),cords))
        y=list(map(lambda x:x[0].strip(),cd))
        x=list(map(lambda x:x[1].strip(),cd))
        pd.DataFrame({'y':y,'x':x}).to_csv(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'.csv', index=False)
    else:
        print(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'.csv already exists')  
    
    if Dup_pass(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'result_korea.csv')==False:
        df=pd.read_csv(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'.csv')
        res=df[(df["x"]>33.0640)&(df["x"]<43.0039)&(df["y"]>124.1100)&(df["y"]<131.5242)]
        res=res[["x","y"]]
        res.to_csv(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'result_korea.csv',index=False)
    else:
        print(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+"result_korea.csv Already Exist")

#_______________________________________________________________________________  
def GeoJSON_cvtr(file,fig):
    CvtrerrorLog=[]
    CvtrerrorLog.append('----------------------------------')
    addr=str(base+'/geojson/WGS84/'+str(file.split('/')[1].split('\\')[1][:-4]))
    global gdf
    if Dup_pass(addr+'.geojson')==False:
        df=pd.read_csv(str(file))
        df=df[df['x']<39]
        points=gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df.y,df.x),crs='epsg:4326')
        joined_points=gpd.sjoin(points,gdf) #실사용용
        #joined_points=points #테스트용
        df_joined_points=pd.DataFrame()
        df_joined_points['x']=joined_points['y']
        df_joined_points['y']=joined_points['x']
        fets=[]
        # create model and prediction
        try:
            dbs=DBSCAN(eps=d,min_samples=3).fit(df_joined_points[['x','y']]).labels_
            df_joined_points=df_joined_points.assign(cluID=dbs)
        except:
            CvtrerrorLog.append((str(file)+"DBSCANwaring: smaple is smaller than minsamples.  Create empty GeoJSON file\n"))
            fets.append('{"type": "Point","coordinates": [0, 0]}')
        else:    
            dbs=DBSCAN(eps=d,min_samples=3).fit(df_joined_points[['x','y']]).labels_        
            df_joined_points=df_joined_points.assign(cluID=dbs)
            for i in range(len(dbs)):
                    data=df_joined_points.loc[df_joined_points.cluID==i]
                    data=data.drop('cluID',axis=1)
                    if len(data)>2:  
                        data_=np.array(data)
                        hull=sp.ConvexHull(data_)
                        #증거 플롯 저장
                        if(fig==True):
                            for simplex in hull.simplices:
                                plt.plot(data_[simplex, 0], data_[simplex, 1], 'k-')                        
                        li=[]
                        for i in hull.vertices:
                            li.append([hull.points[i,0],hull.points[i,1]])
                        li.append(li[0])
                        print(Polygon(li).area)
                        prop_addr,prop_wdir,prop_wspd=getFcst.cord(Polygon(li).centroid)                        
                        prop={"Description":( 
                        "<div style='font-family: gothic, arial, sans-serif;font-size: 15px; font-weight: bold; color:red; margin-bottom: 5px;'>"+str(prop_addr) +"</div><hr/>"+
                        "<div style='font-family: gothic, arial, sans-serif;font-size:15px; font-weight: bold; color:#17002e;'>"+
                            "<table>"+
                                "<tr><td>풍향</td><td>"+str(prop_wdir) +"</td></tr>"+
                                "<tr><td>풍속</td><td>"+str(prop_wspd)+"m/s</td></tr>"+
                                "<tr><td>규모</td><td>"+str(round(Polygon(li).area,4))+"</td></tr>"+
                            "</table>"+
                        "</div>")}
                        geom={ "type": "Polygon","coordinates": [li]}
                        fet={"type": "Feature","geometry":geom,"properties": prop}
                        fets.append(fet) 
            if(fig==True):
                plt.savefig(addr+'.jpg')
                plt.close()
        finally:
            
            dic={"type": "FeatureCollection","features":fets}
            f=open(addr+'.geojson', 'w', encoding='UTF-8-sig')
            f.write(json.dumps(dic, ensure_ascii=False))
            f.close()
            gc.collect(generation=2)
    g=open(base+'/errLog.txt','a', encoding='UTF-8-sig')
    g.write(str(''.join(CvtrerrorLog)))
    g.close()
                
#_______________________________________________________________________________  
def EPSG_cvtr(file):
    if Dup_pass(base+'/geojson/UTMK/'+str(file.split('/')[2].split('\\')[1].split('.')[0])+'UTMK.geojson')==False:
        jsons=gpd.read_file(file)
        jsons=jsons.to_crs('epsg:5179')
        jsons.to_file(base+'/geojson/UTMK/'+str(file.split('/')[2].split('\\')[1].split('.')[0])+'UTMK.geojson', driver='GeoJSON')
#_______________________________________________________________________________      
def DB_insert(file_name):
    if Dup_pass(file_name)==True:
        global conn, curs, insert_time,db_host,db_user,db_pw,db_name,TBLname
        insert_time=file_name.split('/')[2].split('\\')[1].replace("-", " 0").replace("_", "-").split('-')
        insert_time = "-".join(insert_time[0:3])
        print(insert_time)
        TBLname='crdnttable'
        with open(file_name, "r", encoding="utf8") as file:
            contents = file.read()
            json_data = json.loads(contents)
        try:
            # 접속 정보 설정 
            conn = pymysql.connect(host=db_host, user=db_user, password=db_pw, db=db_name, charset='utf8')
            curs = conn.cursor()
        except:
            print("예외2")
            exit()

        dbinsert_num = 0
        sql = "INSERT IGNORE INTO timetable VALUE (\"" + insert_time + "\")"
        curs.execute(sql)
        conn.commit()

        for i in range(len(json_data["features"])):
            coor = (json_data["features"][i]["geometry"]["coordinates"])
            prop = (json_data["features"][i]["properties"]["Description"]) #아래에서 출력하지 않는 것 (공유할 때 생략)
            dbinsert_num += 1
            sql = "INSERT INTO crdnttable(Properties, Coordinates, DataCrawlingTime, prop_ID) value(\"" + prop + "\", \""+ coor +"\", \""+ insert_time +"\"," + str(i) +")"
            curs.execute(sql)
            conn.commit()

        file.close()
        conn.close()
        exit()

#_______________________________________________________________________________    

#######################################
if __name__=='__main__':
    freeze_support()
#    #kml을 한국좌표 추출해 csv변환
#    #data/kml/*.kml -> data/kml_csv_kor_only/*.csv
    with concurrent.futures.ProcessPoolExecutor() as executor:
        imported_files = glob.glob(base+"/kml/*.kml")
        executor.map(CSV_cvtr, imported_files)    
    print('CSV_cvtr Done')
    
    #데이터 필터링 처리해서 WGS84좌표로 GeoJSON 변환
    #data/kml_csv_kor_only/*.csv -> data/geojson/WGS84/*.geojson
    gdf=gpd.read_file(gdfloc).to_crs('epsg:4326') #셰이프파일 위치
    print('gdf load Done')
    imported_files = glob.glob(base+"/kml_csv_kor_only/*result_korea.csv")
    for file in imported_files:
        GeoJSON_cvtr(file,fig_evidence)
    print('GeoJSON_cvtr Done')    
    
    #GeoJSON을 UTMK좌표로 변환
    #data/geojson/WGS84/*.geojson -> data/geojson/UTMK/*.geojson
    with concurrent.futures.ProcessPoolExecutor() as executor:
        imported_files = glob.glob(base+'/geojson/WGS84/*.geojson')
        executor.map(EPSG_cvtr, imported_files)
    print('EPSG_cvtr Done')
        
    #모드 활성화시 DB에 자료 삽입
    #data/geojson/WGS84/*.geojson -> DataBase    
if SQLinsertMode==True:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            imported_files = glob.glob(base+'/geojson/WGS84/*.geojson')    
            executor.map(DB_insert, imported_files)
        print('DB_insert Done')    
######################################            