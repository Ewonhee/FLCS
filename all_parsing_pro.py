import pandas
import json
import os

filepath = 'F:/JS/data.csv'
DataFrame = pandas.read_json("2022_3_23-19selectFireShowList.json")

with open("2022_3_23-19selectFireShowList.json", 'r', encoding='UTF8') as f:
    json_object = json.load(f)

if os.path.isfile(filepath):
    print("파일이 이미 존재하여 변수명들을 추가하지 않습니다.")
    f = open("data.csv", "a")
    f.write("\n")
else:
    print("파일이 존재하지 않아 최초 변수명과 파일을 생성합니다.")
    f = open("data.csv", "a")    
    f.write("화재ID,시작 X좌표,시작 Y좌표,발생일,발생시간,화재 발생 주소,신고 방법,상황,기준 X좌표,기준 Y좌표,업데이트 주소,관측도,관측시,관측기관\n")


# 데이터 사전화, 이름과 값으로 나눔
ForestFireDataName = DataFrame[0]
ForestFireDataValue = DataFrame[1]

# 데이퍼 프레임화, 하나의 열로 표현
tempDF1 = pandas.DataFrame(dict(ForestFireDataName))
tempDF2 = pandas.DataFrame(dict(ForestFireDataValue))

# 행과 열을 전환
a = pandas.DataFrame.transpose(tempDF1)
b = pandas.DataFrame.transpose(tempDF2)

# 2개의 행을 합쳐
ForestFireDataSaved = pandas.merge(a, b, left_on=None)

for i in range (DataFrame.shape[1]):
    SavedData = pandas.DataFrame(dict(DataFrame[i])).transpose()
    
jsonToCSV_FileName = open("allparsingfile.csv", "a")
pandas.to_csv
f.write(SavedData)
print(SavedData)
