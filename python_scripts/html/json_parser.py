import glob
import json
def json_parser(file):
    #파일(json) 위치를 수정해야합니다.
    with open(file, 'r', encoding='UTF8') as f:
        json_object = json.load(f)
    f = open(file.split('\\')[1][:-5]+".csv", "w")
    f.write("신고주소,신고날짜,신고시간,신고타입,신고타입내용,진행상황,진행환료시간,X좌표,Y좌표,확인된주소,관리기관\n")
    #필요한 변수명이 있다면 뒤로 추가합니다. (추가하였으면 위에 헤더로 추가해줍니다.)
    VariableList = ['frfrSttmnAddr', 'frfrSttmnDt', 'frfrSttmnHms', 'frfrOccrrTpcd', 'frfrOccrrTpcdNm', 'frfrPrgrsStcdNm', "potfrCmpleDtm", 'stndaXcrd', 'stndaYcrd', 'frfrUpdtAddr', 'mnoffNm']
    first_data_list = []
    second_data_list = []
    #2개의 집합? 으로 이루어져있어 2개만 추출했습니다.
    for temp in range(0, 2):
        if (temp == 0):
            for Variable in VariableList:
                first_data_list.append(json_object[0][temp][Variable])
        if (temp == 1):
            for Variable in VariableList:
                second_data_list.append(json_object[0][temp][Variable])
    #첫번째 집합? 에서 추출한 내용을 CSV 파일 형식으로 저장합니다.
    for temp in range(len(first_data_list)):
        f.write(first_data_list[temp] + ',')
    #첫번째 집합? 을 모두 출력하여 다음줄로 표현합니다.
    f.write('\n')
    for temp in range(len(second_data_list)):    
        f.write(second_data_list[temp] + ',')
    f.close()
    #확인하기 위해 사용한 print문 입니다.
    print(first_data_list)
    print(second_data_list)
imported_files=glob.glob('test/json/*.json')
for files in imported_files:
    json_parser(files)

