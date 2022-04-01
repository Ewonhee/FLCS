#KML파일분석기 
#출력은 x,y로 구분되는 csv파일
#데이터와 동일위치에 있어야함
#mode True as Korea, False as Samchok

import os
import glob
import concurrent.futures
from bs4 import BeautifulSoup as bs
import pandas as pd
#######################################
mode=False
#######################################
def analysis(file):
    if os.path.isfile('proc/'+str(file[:-4])+'.csv')==False:
        df=pd.DataFrame()
        fr = open(str(file), 'r') 
        lines =fr.read() 
        fr.close()
        xmls=bs(lines, 'html.parser')
        cords=xmls.findAll('coordinates')
        for cord in cords:
            cord.string=cord.string.lstrip('<coordinates>').rstrip('</coordinates>')
            coord=cord.string.split(',')
            df = df.append({'y':coord[0].strip(),'x':coord[1].strip()}, ignore_index=True)
            df.to_csv('proc/'+str(file[:-4])+'.csv', index=False)
    else:
        print('proc/'+str(file[:-4])+'.csv already exists')  
    if mode == False:
        if os.path.isfile('proc/'+str(file[:-4])+"result_korea.csv")==False:
            df=pd.read_csv('proc/'+str(file[:-4])+'.csv')
            res=df[(df["x"]>33.0640)&(df["x"]<43.0039)&(df["y"]>124.1100)&(df["y"]<131.5242)]
            res=res[["x","y"]]
            res.to_csv('proc/'+str(file[:-4])+"result_korea.csv",index=False)
            print("proc/"+str(file[:-4])+"result_korea.csv Successfully Processed")
        else:
            print("proc/"+str(file[:-4])+"result_korea.csv Already Exist")
    else:
        if os.path.isfile('proc/'+str(file[:-4])+"result_Samchok.csv")==False:
            df=pd.read_csv('proc/'+str(file[:-4])+'.csv')
            res=df[(df["x"]>37.0210)&(df["x"]<37.2826)&(df["y"]>128.5701)&(df["y"]<129.2158)]
            res=res[["x","y"]]
            res.to_csv('proc/'+str(file[:-4])+"result_korea.csv",index=False)
            print("proc/"+str(file[:-4])+"result_Samchok.csv Successfully Processed")
        else:
            print("proc/"+str(file[:-4])+"result_Samchok.csv Already Exist")

#_______________________________________________________________________________  
##MAIN_start
  
if(os.path.isdir('proc/')==False):
    os.makedirs('proc/')  
            
#멀티스레딩적용(cpu과부하에 유의)
with concurrent.futures.ProcessPoolExecutor() as executor:
    imported_files = glob.glob("*.kml")
    executor.map(analysis, imported_files)

#싱글스레드
#imported_files = glob.glob("*.kml")
#for file in imported_files:
#    analysis(file)