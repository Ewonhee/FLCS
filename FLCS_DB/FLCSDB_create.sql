# < 빠른 주석 해제는 드래그 후 [CTRL + /] >

CREATE DATABASE IF NOT EXISTS FLCSDB;
USE FLCSDB;

CREATE TABLE IF NOT EXISTS TimeTable (
	DataCrawlingTime DATETIME NOT NULL,
    PRIMARY KEY(DataCrawlingTime)
    );

CREATE TABLE IF NOT EXISTS CrdntTable (
	ID int,
    crdnt_X VARCHAR(50),
    crdnt_Y VARCHAR(50),
    DataCrawlingTime DATETIME NULL,
    ID_PK int AUTO_INCREMENT,
    FOREIGN KEY(DataCrawlingTime) REFERENCES TimeTable(DataCrawlingTime),
    PRIMARY KEY(ID_PK)
);

# 아래의 코드로 crdnttable의 형태를 확인하십시오
-- desc crdnttable;

-- select * from crdnttable;
-- select * from timetable;


# 테스트용 insert
# timetable에 데이터를 입력할 날짜를 먼저 입력하고, crdnttable에 데이터를 입력합니다.
# ID_PK는 auto_increment로 자동 입력되니 생략하고 insert하도록 합니다.

-- insert into timetable value ("2022-03-31 23:30:00");
-- insert into timetable value ("2022-04-01 01:30:00");
-- insert into timetable value ("2022-04-11 06:00:00");

-- insert into crdnttable(ID, crdnt_X, crdnt_Y, DataCrwlingTime) value (1, 123456789, 789456123, "2022-05-06 09:00:00");
-- insert into crdnttable(ID, crdnt_X, crdnt_Y, DataCrwlingTime) value (1, 123456789, 789456123, "2022-05-06 09:00:00");
-- insert into crdnttable(ID, crdnt_X, crdnt_Y, DataCrwlingTime) value (2, 123456789, 789456123, "2022-05-06 09:00:00");
-- insert into crdnttable(ID, crdnt_X, crdnt_Y, DataCrwlingTime) value (2, 123456789, 789456123, "2022-05-06 09:00:00");
-- insert into crdnttable(ID, crdnt_X, crdnt_Y, DataCrwlingTime) value (1, 123456789, 789456123, "2022-05-19 12:00:00");
-- insert into crdnttable(ID, crdnt_X, crdnt_Y, DataCrwlingTime) value (1, 123456789, 789456123, "2022-05-19 12:00:00");
-- insert into crdnttable(ID, crdnt_X, crdnt_Y, DataCrwlingTime) value (1, 123456789, 789456123, "2022-05-19 15:00:00");
-- insert into crdnttable(ID, crdnt_X, crdnt_Y, DataCrwlingTime) value (1, 123456789, 789456123, "2022-05-19 15:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");