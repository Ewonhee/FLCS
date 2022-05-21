import json
import googlemaps
# api key
gmaps = googlemaps.Client(key='mykey')
# 좌표입력
reverse_geocode_result = gmaps.reverse_geocode((36.77519, 126.63483), language='ko')
#print(reverse_geocode_result)
with open('users.json', 'w') as f:
  json.dump(reverse_geocode_result, f)

#저장한 json 파일 불러오기
with open('users.json', 'r', encoding='UTF8') as f:
    json_object = json.load(f)

#불러온 json 파일에서 주소만 가져와 출력하기
print(json_object[0]['formatted_address'])