import glob
from timeit import default_timer as timer
import pandas as pd
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import concurrent.futures
from multiprocessing import freeze_support
df1=None
df2=None
t1=[]
t2=[]
t_s=[]

#새 방식
def test1(file):                              
    global df1 
    fr = open(str(file), 'r') 
    lines =fr.read() 
    fr.close()
    xmls=bs(lines, 'html.parser')
    cords=xmls.findAll('coordinates')
    cd=list(map(lambda x:x.string.split(','),cords))
    y=list(map(lambda x:x[0].strip(),cd))
    x=list(map(lambda x:x[1].strip(),cd))
    df1=pd.DataFrame({'y':y,'x':x})

#기존 사용되던 방식    
def test2(file):
    global df2
    df2=pd.DataFrame()
    fr = open(str(file), 'r') 
    lines =fr.read() 
    fr.close()
    xmls=bs(lines, 'html.parser')
    cords=xmls.findAll('coordinates')
    for cord in cords:
        cord.string=cord.string.lstrip('<coordinates>').rstrip('</coordinates>')
        coord=cord.string.split(',')
        df2 = df2.append({'y':coord[0].strip(),'x':coord[1].strip()}, ignore_index=True)#FW발생

if __name__ == '__main__':
    freeze_support()
    imported_files = glob.glob("C:/Users/SON/FLCS-1/test/kml/*.kml")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for dt in imported_files:
            start = timer()
            test1(dt)
            t1.append(timer()-start)
            start = timer()
            test2(dt)
            t2.append(timer()-start)
            t_s.append(df1.equals(df2))       
    plt.plot(t1,label='new')
    plt.plot(t2,label='old')
    plt.legend()
    print('new',t1)
    print('old',t2)
    #nan to yes
    print('Integrity check',t_s)
    plt.show()
