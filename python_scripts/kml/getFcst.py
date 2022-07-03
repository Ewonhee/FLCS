import math
import json
import googlemaps
import datetime
import requests
import warnings

warnings.filterwarnings('ignore')
##https://velog.io/@chaeri93/Django-%EA%B8%B0%EC%83%81%EC%B2%AD-%EB%8B%A8%EA%B8%B0%EC%98%88%EB%B3%B4-API-%ED%99%9C%EC%9A%A9%ED%95%98%EA%B8%B0
NX = 149            ## X축 격자점 수
NY = 253            ## Y축 격자점 수
Re = 6371.00877     ##  지도반경
grid = 5.0          ##  격자간격 (km)
slat1 = 30.0        ##  표준위도 1
slat2 = 60.0        ##  표준위도 2
olon = 126.0        ##  기준점 경도
olat = 38.0         ##  기준점 위도
xo = 210 / grid     ##  기준점 X좌표
yo = 675 / grid     ##  기준점 Y좌표
first = 0
if first == 0 :
    PI = math.asin(1.0) * 2.0
    DEGRAD = PI/ 180.0
    RADDEG = 180.0 / PI
    re = Re / grid
    slat1 = slat1 * DEGRAD
    slat2 = slat2 * DEGRAD
    olon = olon * DEGRAD
    olat = olat * DEGRAD
    sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(PI * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(PI * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)
    first = 1
    
def mapToGrid(lat, lon):
    ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > PI :
        theta -= 2.0 * PI
    if theta < -PI :
        theta += 2.0 * PI
    theta *= sn
    x = (ra * math.sin(theta)) + xo
    y = (ro - ra * math.cos(theta)) + yo
    x = int(x + 1.5)
    y = int(y + 1.5)
    return x, y

def wdir_cvtr(deg):
    val=float(deg)
    if val<22.5:
        return "북"
    elif val<67.5:
        return "북동"
    elif val<112.5:
        return "동"
    elif val<157.5:
        return "남동"
    elif val<202.5:
        return "남"
    elif val<247.5:
        return "남서"
    elif val<292.5:
        return "서"
    elif val<337.5:
        return "북서"
    elif  val<361:
        return "북"
    
def cord(coord):
    dte=[datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,datetime.datetime.today().hour]
    ymdh=list(map(lambda x:str(x).zfill(2),dte))    
    fct_x,fct_y=mapToGrid(round(coord.y,5),round(coord.x,5))
    #print('위도경도'+str(round(coord.x,5)),str(round(coord.y,5)))
    #print('기상청좌표'+str(fct_x)+","+str(fct_y))
    URL=r"https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey=76QKNWkkWUaT1hqtYhBGwbRq2UVAlf5TczXOf5gEHz68d9N32AmMbkl0gtqU5TBuvECZQhhNUj2zTHxgjiGF7w%3D%3D&pageNo=1&numOfRows=1000&dataType=JSON&base_date="+str("".join(ymdh[0:3]))+"&base_time=0000&nx="+str(fct_x)+"&ny="+str(fct_y)
    try:
        jsn = requests.get(URL.format(),verify=False).json()
        #print(URL)
        #print(jsn)
    except:
        fct_info=dict(WSD="error",VEC="error")
    else:    
        fct_info=dict(map(lambda x: (x['category'],x['obsrValue']),jsn['response']['body']['items']['item']))
    finally:        
        gmaps = googlemaps.Client(key='AIzaSyAcxJTWmScJFuBBsylcl6k4T0_mZST0yto')
        reverse_geocode_result = gmaps.reverse_geocode((round(coord.y,5), round(coord.x,5)), language='ko')
        with open('users.json', 'w', encoding='utf-8') as f:
          json.dump(reverse_geocode_result, f)
        with open('users.json', 'r', encoding='utf-8') as f:
            json_object = json.load(f)
        #print(str("".join(ymdh)))
        #print(str(json_object[0]['formatted_address']))
        #print(fct_info["VEC"]+fct_info["WSD"])
        
        return str(json_object[0]['formatted_address']),wdir_cvtr(fct_info["VEC"]),fct_info["WSD"]