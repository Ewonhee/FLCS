create database captestdb;

use captestdb;

create table tbl1(
	dataCrawlingTime DATETIME NOT NULL,
    primary key(dataCrawlingTime)
);

create table tbl2(
	ID int AUTO_INCREMENT,
	x_coordinates varchar(30),
    y_coordinates varchar(30),
    dataTime DATETIME NULL,
    primary key (ID),
    foreign key(dataTime) references tbl1(dataCrawlingTime)
);

select * from tbl2;

drop DATABASE captestdb;