import matplotlib.pyplot as plt
import pandas as pd
import scipy.spatial as sp
from sklearn.cluster import KMeans
import math

def doit(df_,d):
    clu_id=0
    clu_buffer=[]
    df=df_.sort_values(['y'],ascending=True)
    df=df.reset_index(drop=True)
    for i in range(len(df)):
        if(i != 0):
            buf=df.loc[i]-df.loc[i-1]
        else:
            clu_buffer.append(clu_id)
            continue          
        c = math.sqrt((buf.x * buf.x) + (buf.y * buf.y))
        if(c>d):
            clu_id=clu_id+1
        clu_buffer.append(clu_id)
        print (df.loc[i], clu_id) 
    df=df.assign(cluID=clu_buffer)
    for i in range(clu_id):
        data=df.loc[df.cluID==i]
        data=data.drop('cluID',axis=1).values
        if len(data)>2: 
            #plt.scatter(data[:,1],data[:,0])
            hull=sp.ConvexHull(data)
            for simplex in hull.simplices:
                plt.plot(data[simplex, 1], data[simplex, 0], 'k-')
                
    plt.show()            

#분석대상    
df=pd.read_csv('/home/sons/FLCS/datas/kml_csv_kor_only/2022_3_29-12_J1_VIIRS_C2_result_korea.csv')
#발생화재수(가정임으로 수동력)
d=0.016
doit(df,d)