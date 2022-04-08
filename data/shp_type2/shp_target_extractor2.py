#셰이프파일에서 임분지역만을 추출
#셰이프파일 하위폴더가있는 폴더내에서 실행할것
#메모리 초과로 인해 기본 싱글스레드작동-차후수정-
import geopandas as gpd
import matplotlib.pyplot as plt
import glob
import os
import concurrent.futures

def Extract_geo_data(file_path):
    try:
        gdf=gpd.read_file(file_path,encoding='euc-kr')
        gdf_mt=gdf[(gdf['FIFTH_FRTP']!='W')&(gdf['FIFTH_FRTP']!='R') & (gdf['FIFTH_FRTP'] != '99')][['FIFTH_FRTP','geometry']]
        gdf_mt['nonType']=0
        res=gdf_mt.dissolve(by='nonType')
        try:
            res.to_file('asset/'+str(gdf.SD_NM[0])+".shp")
        except:
            res.to_file('asset/'+str(file_path.split('/')[2])+".shp")    
        res.plot()
        plt.show()
    except:
        print("Error Occured in " + file_path)    

#_______________________________________________________________________________  
##MAIN_start
if(os.path.isdir('asset/')==False):
    os.makedirs('asset/')  
            
#멀티스레딩적용(cpu과부하에 유의)
#with concurrent.futures.ProcessPoolExecutor() as executor:
#    imported_files = glob.glob("**/*.shp", recursive=True)
#    executor.map(Extract_geo_data, imported_files)
#
for file in glob.glob("**/*.shp", recursive=True):
    Extract_geo_data(file)
    
    
#def Extract_geo_data(file_path):
#    gdf=gpd.read_file(file_path,encoding='euc-kr')
#    gdf_mt=gdf[(gdf['FIFTH_FRTP']!='W')&(gdf['FIFTH_FRTP']!='R') & (gdf['FIFTH_FRTP'] != '99')][['FIFTH_FRTP','geometry']]
#    gdf_mt['nonType']=0
#    res=gdf_mt.dissolve(by='nonType')
#    try:
#        res.to_file('GEOproc/'+str(gdf.SD_NM[0])+".shp")
#    except:
#        res.to_file('GEOproc/'+str(file_path.split('/')[2])+".shp")    
#    res.plot()
#    plt.show()
        