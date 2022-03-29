#KML파일분석기 
#출력은 x,y로 구분되는 csv파일
import os
from bs4 import BeautifulSoup as bs
import pandas as pd
mode=False
#분석대상폴더입력
files=os.listdir('C:/Users/SON/Desktop/cap_data/datas')
df=pd.DataFrame()
for file in files:
    if(file[-3:]=='kml'):
        fr = open('C:/Users/SON/Desktop/cap_data/datas/'+str(file), 'r') 
        lines =fr.read() 
        fr.close()
        xmls=bs(lines, 'html.parser')
        cords=xmls.findAll('coordinates')
        for cord in cords:
            cord.string=cord.string.lstrip('<coordinates>').rstrip('</coordinates>')
            coord=cord.string.split(',')
            df = df.append({'y':coord[0].strip(),'x':coord[1].strip()}, ignore_index=True)
        #True as Korea, False as Samchok
        if mode == False:
            res=df[(df["x"]>33.0640)&(df["x"]<43.0039)&(df["y"]>124.1100)&(df["y"]<131.5242)]
            res=res[["x","y"]]
            res=res.reset_index(drop=True)
            res.to_json(str(file[:-4])+"result_korea.json")
        else:
            res=df[(df["x"]>37.0210)&(df["x"]<37.2826)&(df["y"]>128.5701)&(df["y"]<129.2158)]
            res=res[["x","y"]]
            res=res.reset_index(drop=True)
            res.to_json(str(file[:-4])+"result_Samchok.json")

