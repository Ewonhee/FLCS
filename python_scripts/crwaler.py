import requests
import time

result=''

secs = time.time()
tm = time.localtime(secs)
timeStamp=str(tm.tm_year)+'_'+str(tm.tm_mon)+'_'+str(tm.tm_mday)+'-'+str(tm.tm_hour)


SUOMI_VIIRS_C2_Url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/kml/SUOMI_VIIRS_C2_Russia_Asia_24h.kml'
try:
    SUOMI_VIIRS_C2_file = requests.get(SUOMI_VIIRS_C2_Url, allow_redirects=True)
    open(timeStamp+'_SUOMI_VIIRS_C2.kml', 'wb').write(SUOMI_VIIRS_C2_file.content)
except:
    result.append('SUOMI_VIIRS_C2_file_error\n')

     
J1_VIIRS_C2_Url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/kml/J1_VIIRS_C2_Russia_Asia_24h.kml'        
try:    
    J1_VIIRS_C2_file = requests.get(J1_VIIRS_C2_Url, allow_redirects=True)
    open(timeStamp+'_J1_VIIRS_C2_.kml', 'wb').write(J1_VIIRS_C2_file.content)
except:
    result.append('J1_VIIRS_C2_file_error\n')

if(result!=''):
    open(timeStamp+'errorlog.txt','w').write(result)


