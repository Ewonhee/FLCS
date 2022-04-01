import json
import os.path
import csv
import pymysql
import time
import pandas as pd

#CSV파일경로                                (실사용시 변경필요)******************************
ROOT_DIR='/dummy_data/032818/'
#CSV파일명                                  (실사용시 _J1_VIIRS_C2_result_korea추가필요)******************************
CSV='_SUOMI_VIIRS_C2result_korea.csv'
#테이블명
TBLname='crdnttable'

                                            #실사용시 주석해제 및 더미값 제거******************************
#스크립트 시작시간을 기준으로 timeStamp 로드
#tm = time.localtime(time.time())
#timeStamp=str(tm.tm_year)+'_'+str(tm.tm_mon)+'_'+str(tm.tm_mday)+'-'+str(tm.tm_hour)
timeStamp='2022_3_28-18'

pd.read_csv(ROOT_DIR+timeStamp+CSV)    
# csv 파일을 불러와서 mysql의 capstondb-crdnttable의 각각의 colum에 저장.
def insert_proc(root,fName,TBL):
    try:
        sql = "insert into "+str(TBL)+"(crdnt_X, crdnt_Y) value (%s, %s)"
        f = open(root+timeStamp+fName, 'r', encoding='utf-8')
        rdr = csv.reader(f) 
        for line in rdr:
            print(line[0])
            print(line[1])
            val = (line[0], line[1])
            curs.execute(sql, val)
            conn.commit()
        f.close()
    except:
        return
#__________________________________

#main Starts Here      
try:
    # 접속 정보 설정 pw는 임의로 설정됨
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='capstondb', charset='utf8')
    curs = conn.cursor()
except:
    exit()
insert_proc(ROOT_DIR,CSV,TBLname)
conn.close()
exit()