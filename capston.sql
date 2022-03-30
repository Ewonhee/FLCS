create database captestdb;

use captestdb;

drop table tbl1;
drop table tbl2;
drop table tbl3;

create table tbl1(
	dataCrawlingTime DATETIME NOT NULL,
    primary key(dataCrawlingTime)
);

create table tbl2(
	x_coordinates varchar(30),
    y_coordinates varchar(30),
    dataTime DATETIME NOT NULL,
    primary key(x_coordinates, y_coordinates),
    foreign key(dataTime) references tbl1(dataCrawlingTime)
);



create table tbl3(
	화재ID 			varchar(10) not null,
	시작X좌표		varchar(50),
	시작Y좌표		varchar(50),
	발생일			date,
	발생시간		datetime,
	화재발생주소 	text,
	신고방법		varchar(40),
	상황			varchar(20),
	기준X좌표		varchar(50),
	기준Y좌표		varchar(50),
	업데이트주소	text,
	관측도 		varchar(10),
	관측시 		varchar(10),
	관측기관 		varchar(30),
    dataTime DATETIME,
	PRIMARY KEY (화재ID),
    foreign key(dataTime) references tbl1(dataCrawlingTime)
);

insert into tbl1 values("2022-03-30 00:00:00");
insert into tbl1 values("2022-03-30 03:00:00");
insert into tbl1 values("2022-03-30 06:00:00");
insert into tbl1 values("2022-03-30 09:00:00");
insert into tbl1 values("2022-03-30 12:00:00");
insert into tbl1 values("2022-03-30 15:00:00");
insert into tbl1 values("2022-03-30 18:00:00");
insert into tbl2 values("123.12345643", "36.123124124", "2022-03-30 00:00:00");

insert into tbl3 values
(
	115508,
    216963,
    572359,
    20220323,
    190106,
    "경기도 남양주시 진접읍 부평리 266-1",
    "119 신고",
    "진화중",
    "972909.3837279467",
    "1972397.1291250053",
    "경기도 남양주시 진접읍 부평리 266-1",
    "경기도",
    "남양주시",
    "서울국유림관리소",
    "2022-03-30 00:00:00"
);

select * from tbl1;
select * from tbl2;
select * from tbl3;

create view view1 as select 시작X좌표, 시작Y좌표, 발생시간, 관측기관 from tbl3;

select * from view1;

# selectFireShowList 변수 리스트
create table FireListTable(
	cntFireReport bool,
    cntFireExtinguish,
    cntFireCompletion,
    cntFireExceptionEnd,
    cntFire119,
    frfrOccrrPbmrl,
    frfrInfoId,
    frfrSttmnLctnXcrd,
    frfrSttmnLctnYcrd,
    frfrLctnXcrd,
    frfrLctnYcrd,
    frfrSttmnDt,
    frfrSttmnHms,
    frfrSttmnAddr,
    frfrOccrrTpcd,
    frfrOccrrTpcdNm,
    frfrOccrrStcd,
    frfrOccrrWindrcCd,
    ffrwtTrmnlId,
    dltYn,
    frfrPrgrsStcd,
    frfrPrgrsStcdNm,
    frfrSttmnDtm,
    frstRgterId,
    lastUpusrId,
    lgdngCd,
    pinchTlno,
    trnsnYn,
    potfrCmpleDtm,
    frfrStepIssuSeq,
    frfrStepIssuDtm,
    frfrStepIssuCd,
    frfrStepIssuNm,
    pnuCd,
    stndaXcrd,
    stndaYcrd,
    frfrUpdtAddr,
    wtherLttcId,
    lcltFrsrvInsttCd,
    ntfrtMnoffInsttCd,
    ctpKorNm,
    sggNm,
    mnoffNm,
    riskTpcd,
    distinct,
    page,
    rows,
    sord,
    floatData,
    floatDataDelim,
    paging,
    currentPageNo,
    recordCountPerPage,
    pageSize,
    totalRecordCount,
    totalPageCount,
    firstPageNoOnPageList,
    lastPageNoOnPageList,
    firstRecordIndex,
    lastRecordIndex
);



# asd.csv 리스트
create table FireListTable(
	cntFire119,
	cntFireCompletion,
	cntFireExceptionEnd,
	cntFireExtinguish,
	cntFireReport,
	ctpKorNm,
	currentPageNo,
	distinct,
	dltYn,
	ffrwtTrmnlId,
	firstPageNoOnPageList,
	firstRecordIndex,
	floatData,
	floatDataDelim,
	frfrInfoId,
	frfrLctnXcrd,
	frfrLctnYcrd,
	frfrOccrrPbmrl,
	frfrOccrrStcd,
	frfrOccrrTpcd,
	frfrOccrrTpcdNm,
	frfrOccrrWndrcCd,
	frfrPrgrsStcd,
	frfrPrgrsStcdNm,
	frfrStepIssuCd,
	frfrStepIssuDtm,
	frfrStepIssuNm,
	frfrStepIssuSeq,
	frfrSttmnAddr,
	frfrSttmnDt,
	frfrSttmnDtm,
	frfrSttmnHms,
	frfrSttmnLctnXcrd,
	frfrSttmnLctnYcrd,
	frfrUpdtAddr,
	frstRgterId,
	lastPageNoOnPageList,
	lastRecordIndex,
	lastUpusrId,
	lcltFrsrvInsttCd,
	lgdngCd,
	mnoffNm,
	ntfrtMnoffInsttCd,
	page,
	pageSize,
	paging,
	pinchTlno,
	pnuCd,
	potfrCmpleDtm,
	recordCountPerPage,
	riskTpcd,
	rows,
	sggNm,
	sord,
	stndaXcrd,
	stndaYcrd,
	totalPageCount,
	totalRecordCount,
	trnsnYn,
	wtherLttcId,
    primary key(
);

create table testtbl(
fireID 			varchar(10) not null,
시작X좌표		varchar(50),
시작Y좌표		varchar(50),
발생일			date,
발생시간		datetime,
화재발생주소 	text,
신고방법		varchar(40),
상황			varchar(20),
기준X좌표		varchar(50),
기준Y좌표		varchar(50),
업데이트주소	text,
관측도 		varchar(10),
관측시 		varchar(10),
관측기관 		varchar(30),
PRIMARY KEY (화재ID)
);

insert into testtbl values
(
	115508,
    216963,
    572359,
    20220323,
    190106,
    "경기도 남양주시 진접읍 부평리 266-1",
    "119 신고",
    "진화중",
    "972909.3837279467",
    "1972397.1291250053",
    "경기도 남양주시 진접읍 부평리 266-1",
    "경기도",
    "남양주시",
    "서울국유림관리소"
);

select * from testtbl;

create view firstView as select 화재ID, 시작X좌표, 시작Y좌표 from testtbl;

select * from firstView;

drop view firstview;
