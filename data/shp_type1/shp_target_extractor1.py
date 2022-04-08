#셰이프파일에서 임분지역만을 추출
#셰이프파일 하위폴더가있는 폴더내에서 실행할것
import geopandas as gpd
import matplotlib.pyplot as plt
import glob
import pandas as pd
import os
import concurrent.futures
mg=gpd.GeoDataFrame({'UCB':[],'geometry':[]})
def Extract_geo_data(file_path):
    try:
        gdf=gpd.read_file(file_path,encoding='euc-kr')
    except:
        print(file_path+'에서 에러발생')
        return
    gdf=gpd.read_file(file_path,encoding='euc-kr')
    try:        
        gdf_mt=gdf[(gdf['UCB']=='2230')|(gdf['UCB']=='2210') | (gdf['UCB'] == '2220')][['UCB','geometry']]
        print(file_path+'에서 1T로 임분지역만 추출')
        gdf_mt.to_file('asset/'+file_path.split('/')[0]+'.shp')
    except:
        gdf_mt=gdf[(gdf['ucb']=='2230')|(gdf['ucb']=='2210') | (gdf['ucb'] == '2220')][['ucb','geometry']]
        print(file_path+'에서 2T로 임분지역만 추출')
        gdf_mt.to_file('asset/'+file_path.split('/')[0]+'.shp')
    
with concurrent.futures.ProcessPoolExecutor() as executor:
    imported_files = glob.glob("**/*.shp", recursive=True)
    executor.map(Extract_geo_data, imported_files)