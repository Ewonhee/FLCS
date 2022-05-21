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
import json
import pymysql
import matplotlib.pyplot as plt

#KML파일분석기 
#최상위디렉터리에서 수행되어야함
#######################################
# T  O  D  O   L  I  S  T #
    #GeoJSON_cvtr:JSON모듈활용해 개량할것 (0509)
    #동수형 코드 수정될시 보수작업
# N  O  T  E   L  I  S  T #    
    #GeoJSON_cvtr: concurrnt.futures로 병렬처리 오류발생(실사용시 문제 없음)
#######################################
# P  A  N  E  L #
d=0.10                                                                                           #d-value
base="test"                                                                                    #베이스 폴더 지정[test, data]
mp=True                                                                                       #멀티프로세싱 사용여부
fig_evidence=True                                                                         #증거용플롯저장
db_host='localhost'                                                                        #DB호스트
db_user='root'                                                                                #DB유저
db_pw='1234'                                                                                 #DBPW
db_name='flcsdb'                                                                            #DB명
TBLname='crdnttable'                                                                    #테이블명
gdfloc='data/korea_forest_map.shp'                                               #셰이프파일 위치
conn,curs,insert_time=None,None,None                                        #DB용 전역변수 (시험용도외 건들지말것
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
    addr=str(base+'/geojson/WGS84/'+str(file.split('/')[1].split('\\')[1][:-4]))
    global gdf
    if Dup_pass(addr+'.geojson')==False:
        df=pd.read_csv(str(file))
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
            print(str(file)+"DBSCAN경고: smaple이 minsamples보다 작습니다. 비어있는 GeoJSON파일을 생성합니다")
            out='{"type": "Point","coordinates": [0, 0]}'
        else:    
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
                        #증거 플롯 저장
                        if(fig==True):
                            for simplex in hull.simplices:
                                plt.plot(data_[simplex, 0], data_[simplex, 1], 'k-')                        
                        exportJSON=exportJSON+'['
                        for i in hull.vertices:
                            exportJSON=exportJSON+str('['+str(hull.points[i,0])+','+str(hull.points[i,1])+'],')
                            if(cnt<len(hull.vertices)):
                                cnt=cnt+1
                            else:
                                exportJSON=exportJSON+str('['+str(hull.points[hull.vertices[0],0])+','+str(hull.points[hull.vertices[0],1])+']],')
            out='{"type": "MultiPolygon","coordinates": [['+exportJSON[:-1]+']]}'
            if(fig==True):
                plt.savefig(addr+'.jpg')
                plt.close()
        finally:
            f=open(addr+'.geojson','w')
            f.write(out)
            f.close()
            gc.collect(generation=2)
#_______________________________________________________________________________  
def EPSG_cvtr(file):
    if Dup_pass(base+'/geojson/UTMK/'+str(file.split('/')[2].split('\\')[1].split('.')[0])+'UTMK.geojson')==False:
        jsons=gpd.read_file(file)
        jsons=jsons.to_crs('epsg:5179')
        jsons.to_file(base+'/geojson/UTMK/'+str(file.split('/')[2].split('\\')[1].split('.')[0])+'UTMK.geojson', driver='GeoJSON')
#_______________________________________________________________________________  
def insert_proc(coor, TBL, coorID):
    sql = "insert into " + str(TBL) + "(ID, crdnt_X, crdnt_Y, DataCrawlingTime) value (%s, %s, %s, \""+ insert_time + "\")"
    val = (coorID, coor[0], coor[1])
    curs.execute(sql, val)
    print(sql)
    conn.commit()
    return
#_______________________________________________________________________________    
def DB_insert(file_name):
    if Dup_pass(file_name)==True:
        global conn, curs, insert_time,db_host,db_user,db_pw,db_name,TBLname
        insert_time = file_name.split('/')[2].split('\\')[1].replace("-", " 0").replace("_", "-").split('-')
        insert_time = "-".join(insert_time[0:3])
        print("사용된 파일 시간 : " + insert_time)

        TBLname='crdnttable'
        with open(file_name, "r", encoding="utf8") as file:
            contents = file.read()
            json_data = json.loads(contents)
        try:
            # 접속 정보 설정 pw는 임의로 설정됨
            conn = pymysql.connect(host=db_host, user=db_user, password=db_pw, db=db_name, charset='utf8')
            curs = conn.cursor()
        except:
            print("예외2")
            exit()
        # <참고> 
        #   json_loads로 불러온 데이터의 coordinates를 불러오면 coor[0]은 해당 좌표 전체,
        #   coor[0][i]은 해당 좌표 전체의 i번째 좌표, coor[0][i][j]는 해당 좌표 전체의 i번째 j좌표 (x, y) 각각에 접근가능
        dbinsert_num = 0

        # 최초 해당 시간에 데이터를 입력할 때 timetable에 데이터를 저장하기 위한 SQL문
        sql = "insert ignore into timetable value (\"" + insert_time + "\")"
        curs.execute(sql)
        print(sql)
        conn.commit()

        for i in range(len(json_data["features"])):
            coor = (json_data["features"][i]["geometry"]["coordinates"])
            for k in range(len(coor[0])):
                dbinsert_num += 1
                insert_proc(coor[0][k], TBLname, i)
        print("총 DB 삽입 시도 횟수 : " + str(dbinsert_num))
        file.close()
        conn.close()
        exit()
#_______________________________________________________________________________    

#######################################
if __name__=='__main__':
    freeze_support()
    #kml을 한국좌표 추출해 csv변환
    #data/kml/*.kml -> data/kml_csv_kor_only/*.csv
    with concurrent.futures.ProcessPoolExecutor() as executor:
        imported_files = glob.glob(base+"/kml/*.kml")
        if mp==False:
            map(CSV_cvtr, imported_files)
        else:    
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
        if mp==False:
            map(EPSG_cvtr, imported_files)
        else:    
            executor.map(EPSG_cvtr, imported_files)
    print('EPSG_cvtr Done')
    
    #DB에 자료 삽입
    #data/geojson/WGS84/*.geojson -> DataBase    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        imported_files = glob.glob(base+'/geojson/WGS84/*.geojson')
        if mp==False:
            map(DB_insert, imported_files)
        else:    
            executor.map(DB_insert, imported_files)
    print('DB_insert Done')    
######################################            