#한줄로된 html을 여러줄로 바꾸어주는 스크립트

import os
def replace_in_file(file_path, old_str, new_str):
    fr = open(file_path, 'r') 
    lines = fr.readlines() 
    fr.close()
    fw = open(file_path, 'w') 
    for line in lines: 
        fw.write(line.replace(old_str, new_str)) 
    fw.close()
        
files=os.listdir()
for file in files:
    if(file[-4:]=='html'):
        replace_in_file(file,',"',',\n"')
