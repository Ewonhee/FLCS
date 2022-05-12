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
    FOREIGN KEY(DataCrawlingTime) REFERENCES TimeTable(DataCrawlingTime)
);

#아래의 코드로 crdnttable의 형태를 확인하십시오
#desc crdnttable;

select * from crdnttable;
select * from timetable;
insert into timetable value ("2022-03-31 23:30:00");
insert into timetable value ("2022-04-01 01:30:00");
insert into timetable value ("2022-04-11 06:00:00");


-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");
-- insert into crdnttable(crdnt_X, crdnt_Y, DataCrwlingTime) value (123456789, 789456123, "2022-05-06 12:00:00");

    
#alter table crdnttable add column properties varchar(100) not null;