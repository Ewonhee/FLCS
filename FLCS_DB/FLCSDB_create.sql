# DB 생성시 전체 실행하십시오.
# drop database flcsdb;
CREATE DATABASE IF NOT EXISTS FLCSDB;
USE FLCSDB;

CREATE TABLE IF NOT EXISTS TimeTable (
	DataCrawlingTime DATETIME NOT NULL,
    PRIMARY KEY(DataCrawlingTime)
    );

CREATE TABLE IF NOT EXISTS CrdntTable (
    DataCrawlingTime DATETIME NULL,
    Properties VARCHAR(500),
    Coordinates VARCHAR(1000),
    prop_ID int,
    ID_PK int AUTO_INCREMENT,
    FOREIGN KEY(DataCrawlingTime) REFERENCES TimeTable(DataCrawlingTime),
    PRIMARY KEY(ID_PK)
);