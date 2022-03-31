import json
import os.path
import csv
import pymysql
import time

# csv 파일을 불러와서 mysql의 capstondb-crdnttable의 각각의 colum에 저장.

start = time.time()
conn = pymysql.connect(host='localhost', user='root', password='1234', db='capstondb', charset='utf8')
curs = conn.cursor()

sql = "insert into crdnttable(crdnt_X, crdnt_Y) value (%s, %s)"

f = open('2022_3_28-18_SUOMI_VIIRS_C2result_korea.csv', 'r', encoding='utf-8')
rdr = csv.reader(f) 
for line in rdr:
    print(line[0])
    print(line[1])
    val = (line[0], line[1])
    curs.execute(sql, val)
    conn.commit()

#printf("%d", a);

f.close()
conn.close()

print("time : ", time.time() - start) 