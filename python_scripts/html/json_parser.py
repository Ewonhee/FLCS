import glob
import pandas as pd
import matplotlib.pyplot as plt
imported_files = glob.glob("C:/Users/SON/FLCS-1/test/json/*.json")
d=[]
for f in imported_files:
    dat=pd.read_json(f)
    for i in range(dat.size):
        d.append(dict(dat[i][0]))
x=list(map(lambda x:x['stndaXcrd'],d))
y=list(map(lambda x:x['stndaYcrd'],d))
addr=list(map(lambda x:x['frfrUpdtAddr'],d))        
maps=pd.DataFrame([x,y,addr],index=['lat','lon','addr']).T
