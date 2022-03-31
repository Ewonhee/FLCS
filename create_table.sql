CREATE DATABASE IF NOT EXISTS capstonDB;
USE capstonDB;

CREATE TABLE IF NOT EXISTS TimeTable (
	DataCrawlingTime DATETIME NOT NULL,
    PRIMARY KEY(DataCrawlingTime)
    );

CREATE TABLE IF NOT EXISTS CrdntTable (
	ID int AUTO_INCREMENT,
    crdnt_X VARCHAR(50),
    crdnt_Y VARCHAR(50),
    DataCrawlingTime DATETIME NULL,
    PRIMARY KEY(ID),
    FOREIGN KEY(DataCrawlingTime) REFERENCES TimeTable(DataCrawlingTime)
);

#FireShowList 열중에 "distinct, page, rows"는 column으로 생성할 수 없어 주석처리해둠

CREATE TABLE IF NOT EXISTS FireListTable(
	cntFireReport VARCHAR(10),
    cntFireExtinguish VARCHAR(10),
    cntFireCompletion VARCHAR(10),
    cntFireExceptionEnd VARCHAR(10),
    cntFire119 VARCHAR(10),
    frfrOccrrPbmrl VARCHAR(10),
    frfrInfoId VARCHAR(30) NOT NULL,
    frfrSttmnLctnXcrd VARCHAR(50),
    frfrSttmnLctnYcrd VARCHAR(50),
    frfrLctnXcrd VARCHAR(50),
    frfrLctnYcrd VARCHAR(50),
    frfrSttmnDt VARCHAR(50),
    frfrSttmnHms VARCHAR(50),
    frfrSttmnAddr VARCHAR(100),
    frfrOccrrTpcd VARCHAR(10),
    frfrOccrrTpcdNm VARCHAR(30),
    frfrOccrrStcd VARCHAR(10),
    frfrOccrrWindrcCd VARCHAR(10),
    ffrwtTrmnlId VARCHAR(10),
    dltYn VARCHAR(10),
    frfrPrgrsStcd VARCHAR(10),
    frfrPrgrsStcdNm VARCHAR(30),
    frfrSttmnDtm VARCHAR(10),
    frstRgterId VARCHAR(10),
    lastUpusrId VARCHAR(10),
    lgdngCd VARCHAR(50),
    pinchTlno VARCHAR(10),
    trnsnYn VARCHAR(10),
    potfrCmpleDtm VARCHAR(10),
    frfrStepIssuSeq VARCHAR(10),
    frfrStepIssuDtm VARCHAR(10),
    frfrStepIssuCd VARCHAR(10),
    frfrStepIssuNm VARCHAR(10),
    pnuCd VARCHAR(100),
    stndaXcrd VARCHAR(50),
    stndaYcrd VARCHAR(50),
    frfrUpdtAddr VARCHAR(100),
    wtherLttcId VARCHAR(10),
    lcltFrsrvInsttCd VARCHAR(10),
    ntfrtMnoffInsttCd VARCHAR(30),
    ctpKorNm VARCHAR(30),
    sggNm VARCHAR(30),
    mnoffNm VARCHAR(50),
    riskTpcd VARCHAR(10),
    #distinct VARCHAR(10),
    #page VARCHAR(10),
    #rows VARCHAR(10),
    sord VARCHAR(10),
    floatData VARCHAR(10),
    floatDataDelim VARCHAR(10),
    paging VARCHAR(10),
    currentPageNo VARCHAR(10),
    recordCountPerPage VARCHAR(10),
    pageSize VARCHAR(10),
    totalRecordCount VARCHAR(10),
    totalPageCount VARCHAR(10),
    firstPageNoOnPageList VARCHAR(10),
    lastPageNoOnPageList VARCHAR(10),
    firstRecordIndex VARCHAR(10),
    lastRecordIndex VARCHAR(10),
    PRIMARY KEY(frfrInfoId)
);

CREATE VIEW AnalyzedVariableView AS SELECT frfrSttmnDt, frfrSttmnHms, frfrPrgrsStcd, potfrCmpleDtm, 
stndaXcrd, stndaYcrd, frfrUpdtAddr from capstonDB.FireListTable;