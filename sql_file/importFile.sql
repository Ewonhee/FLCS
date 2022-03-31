# sql 보안 문제로 8.0버전에서는 mysql server 파일에 데이터를 넣어야 한다고 합니다.
# secure 파일 확인
SHOW VARIABLES LIKE 'secure_file_priv';

CREATE TABLE foo ( id INT NOT NULL AUTO_INCREMENT, x varchar(30), y varchar(30), PRIMARY KEY (id) );

SET @timeVar= DATE_FORMAT(now(), '%Y_%m_%d_%H');
#앞주소
SET @prefix= concat('C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\',@timeVar);
#뒤주소(파일명)
SET @PATHS=concat(@prefix,'_SUOMI_VIIRS_C2result_korea.csv');

#합친 최종 주소(파일명)
set @filename = CAST(@PATHS as char); 
SELECT @filename;

#오류 발생 부분입니다.. 파일 명을 변수로 못 받습니다.
LOAD DATA INFILE @filename INTO TABLE foo FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
(@x,@y) SET x = @x, y = @y;
#LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\2022_3_28-18_SUOMI_VIIRS_C2result_korea.csv' INTO TABLE foo FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
# (@x,@y) SET x = @x, y = @y;

desc foo;
select * from foo;
drop TABLE foo;