const mysql = require('mysql');  // mysql 모듈 로드
const conn = {  // mysql 접속 설정
    host: 'localhost',
    port: '3306',
    user: 'root',
    password: '1234', // 비밀번호
    database: 'capstondb' // 데이터베이스명
};
var connection = mysql.createConnection(conn); // DB 커넥션 생성
connection.connect();   // DB 접속
// 이하는 데이터베이스 연동 확인 문입니다.
var testQuery = "SELECT JSON_OBJECTAGG(Crdnttable.crdnt_X,Crdnttable.crdnt_Y) FROM capstondb.Crdnttable;";

function getQuery(query){
connection.query(query, function (err, results, fields) { // testQuery 실행
    if (err) {
        //console.log(err);
        console.log('에러발생');
    }
    console.log(results);
});
connection.end(); // DB 접속 종료
}
getQuery(testQuery);

