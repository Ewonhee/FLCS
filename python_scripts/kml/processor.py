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

#KML파일분석기 
#최상위디렉터리에서 수행되어야함
#######################################
# T  O  D  O   L  I  S  T #
    #GeoJSON_cvtr:결과물 플롯 증거로 저장할것
    #GeoJSON_cvtr:JSON모듈활용해 개량할것(0509)
    #pd->FW발생해결 필요
    #동수형 코드 수정될시 보수작업
#######################################
# P  A  N  E  L #
d=0.10                                                                                           #d-value
base="test"                                                                                    #베이스 폴더 지정[test, data]
mp=False                                                                                       #멀티프로세싱 사용여부
db_host='localhost'                                                                        #DB정보
db_user='root'
db_pw='1234'
db_name='flcsdb'
TBLname='crdnttable'
gdf=gpd.read_file('data/korea_forest_map.shp').to_crs('epsg:4326') #셰이프파일 위치
conn,curs,insert_time=None,None,None                                        #시험용도외 건들지말것
#######################################
def Dup_pass(file):
    if os.path.isfile(file):
        return True
    else:
        return False
#_______________________________________________________________________________  
def CSV_cvtr(file):
    if Dup_pass(base+'/kml_csv_kor_only/'+str(file.split('/')[1].split('\\')[1][:-4])+'.csv')==False:
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
def GeoJSON_cvtr(file):
    addr=str(base+'/geojson/WGS84/'+str(file.split('/')[1].split('\\')[1][:-4])+'.geojson')
    global gdf
    if Dup_pass(addr)==False:##### indent matching error
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
            print(str(file)+"DBSCAN오류: smaple이 minsamples보다 작습니다.")
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
        f=open(addr,'w')
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
        insert_time=file_name.split('/')[2].split('\\')[1].replace("-", " 0").replace("_", "-").split('-')
        insert_time = "-".join(insert_time[0:3])
        print(insert_time)
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
        #json_loads로 불러온 데이터의 coordinates를 불러오면
        #coor[0]은 해당 좌표 전체
        #coor[0][i]은 해당 좌표 전체의 i번째 좌표
        #coor[0][i][j]는 해당 좌표 전체의 i번째 j좌표 (x, y) 각각에 접근가능
        dbinsert_num = 0
        for i in range(len(json_data["features"])):
            coor = (json_data["features"][i]["geometry"]["coordinates"])
            prop = (json_data["features"][i]["properties"]) #아래에서 출력하지 않는 것 (공유할 때 생략)
            for k in range(len(coor[0])):
                print(coor[0][k])
                print(TBLname)
                print(i)
                print("\n")
                dbinsert_num+=1
                print("db 삽입 시도 횟수 : " + str(dbinsert_num))
                insert_proc(coor[0][k], TBLname, i)
        #select_sql = "select * from " + TBLname
        select_sql = "select * from crdnttable"
        curs.execute(select_sql)
        result = curs.fetchall()
        print(result)
        # coor = (json_data["features"][0]["geometry"]["coordinates"])
        # with open('test.csv', 'w', newline='') as f:
        #     for i in range(len(coor[0])):
        #         for j in range(len(coor[0][i])):
        #             writer = csv.writer(f)
        #             writer.writerow(coor[0][i][j])
        #insert_proc(ROOT_DIR, CSV, TBLname)
        file.close()
        conn.close()
        exit()
#_______________________________________________________________________________    

#######################################
if mp == True:
    #멀티코어모드(고사양, 실사용)
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
    #싱글코어모드(저사양, 디버깅시)
        imported_files = glob.glob(base+"/kml/*.kml")
        for file in imported_files:
            CSV_cvtr(file)
        imported_files = glob.glob(base+"/kml_csv_kor_only/*.csv")
        for file in imported_files:
            GeoJSON_cvtr(file)
        imported_files = glob.glob(base+'/geojson/WGS84/*.geojson')
        for file in imported_files:
            EPSG_cvtr(file)
        imported_files = glob.glob(base+'/geojson/UTMK/*.geojson')
        for file in imported_files:
            DB_insert(file)        
#######################################            