<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<!DOCTYPE html>
<html>

<head>
<title>tester</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script type="text/javascript" src="https://code.jquery.com/jquery-latest.js"></script>
<script type="text/javascript" src="https://sgisapi.kostat.go.kr/OpenAPI3/auth/javascriptAuth?consumer_key=00ed8bb8f7f946f3b308"></script>
<meta name="type" property="og:type" content="article">
<link rel="stylesheet" type="text/css" media="screen" href="./css/FLCS.css">
<link rel="stylesheet" media="only screen and (min-width:200px) and (max-width:480px)" href="./css/FLCS.css">
<link rel="stylesheet" type="text/css" href="./css/FLCS.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap" rel="stylesheet">
</head>

<%
String sCondition2 = request.getParameter("date");
String sCondition3 = request.getParameter("time");
String num_data = "0";
if (sCondition2 == null)
	sCondition2 = "2022-04-11";
if (sCondition3 == null)
	sCondition3 = "0";
%>
<%@ include file="dbconn.jsp"%>
<%@ page import="java.lang.*"%>
<%
//flcsDB에서 select
ResultSet rs1 = null;
PreparedStatement pstmt1 = null;
ResultSet rs2 = null;
PreparedStatement pstmt2 = null;
ResultSet rs3 = null;
PreparedStatement pstmt3 = null;
StringBuilder sb1 = new StringBuilder();
StringBuilder sb2 = new StringBuilder();
StringBuilder sb3 = new StringBuilder();
String data_count = "";
String addr_div1 = "<div style=\'font-family: gothic, arial, sans-serif;font-size: 15px; font-weight: bold; color:red; margin-bottom: 5px;\'>";
String addr_div2 = "</div><hr/><div style='font-family: gothic, arial, sans-serif;font-size:15px; font-weight: bold; color:#17002e;'><table><tr><td>";
String addr_div3 = "</td><td>";
String addr_div4 = "</td></tr><tr><td>";
String addr_div5 = "</td><td>";
String addr_div6 = "</td></tr></table></div>";
try {
	String sql_prop = "SELECT * FROM crdnttable WHERE DataCrawlingTime = \"" + sCondition2 + " " + sCondition3 + "\"";
	String sql_coor = "SELECT Coordinates FROM crdnttable WHERE DataCrawlingTime = \"" + sCondition2 + " " + sCondition3
	+ "\"";
	String sql_count_date = "SELECT COUNT(*) FROM crdnttable WHERE DataCrawlingTime = \"" + sCondition2 + " "
	+ sCondition3 + "\"";
	pstmt1 = conn.prepareStatement(sql_prop);
	pstmt2 = conn.prepareStatement(sql_coor);
	pstmt3 = conn.prepareStatement(sql_count_date);
	rs1 = pstmt1.executeQuery();
	rs2 = pstmt2.executeQuery();
	rs3 = pstmt3.executeQuery();
	rs3.next();
	num_data = rs3.getString("COUNT(*)");
	for (int i = 0; i < Integer.parseInt(num_data); i++) {
		rs1.next();
		String temp = rs1.getString("Properties");
/* 		String[] temparr = temp.split("<br>");
		String addr = temparr[0].substring(0, temparr[0].length() - 10);
		String[] temparr2 = temparr[1].split(", ");
		String wind_dir = temparr2[0].substring(temparr2[0].length() - 2, temparr2[0].length());
		String wind_speed = temparr2[1].substring(temparr2[1].length() - 3, temparr2[1].length()); */
		String temp2 = rs1.getString("Coordinates");
		sb1.append("{ \"type\": \"Feature\", \"properties\": { \"Description\": \"" + temp + "\"},");
		sb1.append("\"geometry\": { \"type\": \"Polygon\", \"coordinates\": " + temp2 + "} },");
	}
} catch (SQLException ex) {
} finally {
	if (rs1 != null)
		rs1.close();
	if (pstmt1 != null)
		pstmt1.close();
	if (rs2 != null)
		rs2.close();
	if (pstmt2 != null)
		pstmt2.close();
	if (conn != null)
		conn.close();
	if (sb1.length() >= 1)
		sb1.setLength(sb1.length() - 1);
}
%>
<body>
	<div id="set">
		<div id="map" class="map"></div>
		<div id="wrap">
			<header>
				<div class="logo_box">
					<img src="./images/FLCS.png" alt="FLCS">
				</div>
				<ul>
					<!-- menu1: 날짜 선택 -->
					<ul class="menu1">
						<details>
							<summary>
								<a>&#128197;</a>
								<p>시간선택</p>
							</summary>
							<div class="menu1_dateTime">
								<form action="FLCS_main2.jsp" method="get">
									<div id="form">
										<p>
											<input id="date" type="date" name="date" min="2022-03-30" max="2022-05-07" required>
										</p>
										<select name="time" id="time">
											<option value="0">-- 시간 --</option>
											<option value="0">00:00</option>
											<option value="3">03:00</option>
											<option value="6">06:00</option>
											<option value="9">09:00</option>
											<option value="12">12:00</option>
											<option value="15">15:00</option>
											<option value="18">18:00</option>
											<option value="21">21:00</option>
											<option value="24">24:00</option>
										</select>
										<p>
											<input id="submitId" type="submit" value="Ok">
										</p>
									</div>
								</form>
							</div>
						</details>
					</ul>
					<!-- menu2: 파일로 다운로드 -->
					<ul class="menu2">
						<details>
							<summary>
								<a>&#128229;</a>
								<p>다운로드</p>
							</summary>
							<div class="menu2_dateTime">
								<div id="form">
									<p>
										<input id="ddate" type="date" min="2022-03-30" max="2022-05-07" required>
									</p>
									<select name="time" id="dtime">
										<option value="0">-- 시간 --</option>
										<option value="0">00:00</option>
										<option value="3">03:00</option>
										<option value="6">06:00</option>
										<option value="9">09:00</option>
										<option value="12">12:00</option>
										<option value="15">15:00</option>
										<option value="18">18:00</option>
										<option value="21">21:00</option>
										<option value="24">24:00</option>
									</select>
								</div>
								<a href="/2022_3_30-6_SUOMI_VIIRS_C2result_koreaUTMK.geojson" id="pt" download="test.txt" onclick="dinput()">다운로드</a>
							</div>
						</details>
					</ul>
					<ul class="menu3">
						<p style="font-size: 9px; vertical-align: bottom; text-align: center;"><%=sCondition2%></p>
						<p style="font-size: 9px; vertical-align: bottom; text-align: center;"><%=sCondition3%>시</p>
						<p style="font-size: 9px; vertical-align: bottom; text-align: center;">산불<%=num_data%>개</p>
					</ul>
				</ul>
			</header>
		</div>
	</div>

	<script>
 //현재 날짜까지만 선택할 수 있게 제한
  document.getElementById('date').setAttribute("max", new Date().toISOString().substring(0, 10));
  document.getElementById('ddate').setAttribute("max", new Date().toISOString().substring(0, 10));

 //날짜 선택하였을때 불러오는 함수
 function input() {
    var date = document.querySelector("#date").value;
    var time = document.querySelector("#time").value;
    console.log(date+" "+time);
  }
 
  //2022_3_30-6_SUOMI_VIIRS_C2result_koreaUTMK.geojson
 function dinput() {
  var ddate = document.querySelector("#ddate").value;
  var dtime = document.querySelector("#dtime").value;
  var [year, mmonth, date] = ddate.split('-');
  var month;
  if(mmonth.startsWith('0')){
	  month = parseInt(mmonth.substring(0,2));
  }
  else{
	  month=parseInt(mmonth);
  }
  if(date.startsWith('0')){
	  date = parseInt(date.substring(0,2));
  }
  else{
	  date=parseInt(date);
  }
/*   var month=parseInt(mmonth); */
   month=String(month);

   document.getElementById('pt').setAttribute("download", ddate+"-"+dtime);
   document.getElementById('pt').setAttribute("href", "./data/"+year+"_"+month+"_"+date+"-"+dtime+"_SUOMI_VIIRS_C2result_koreaUTMK.geojson");

   console.log(+year+"_"+month+"_"+date+"-"+dtime+"_SUOMI_VIIRS_C2result_koreaUTMK.geojson");
  }
 function handler(e){
	  alert(e.target.value);
	}


var map = sop.map("map");
map.setView(sop.utmk(1123909.053995, 1906854.9295), 1);
var LOCdatas = new Array();
var INFOdatas = new Array();
var HeatCoordDatas = new Array();
var myHeatCoordDatas = new Array();

var heatmapCoord="미사용"
var jsonData="보수중"
//2022_4_11-21_J1_VIIRS_C2_result_koreaEPSG
var geoData = {
			"type" : "FeatureCollection",
			"crs" : {
				"type" : "name",
				"properties" : {
					"name" : "urn:ogc:def:crs:EPSG::5179"
				}
			},
			"features" : [
	<%=sb1%>
		]
		};
sop.geoJson(geoData, {
 style: function () {
  return {
   weight: 0.5,
   opacity: 1,
   color: '#FF0000',
   dashArray: '0',
   fillOpacity: 0.4
  };
 },
 onEachFeature: function (feature, layer) {
  layer.bindInfoWindow(feature.properties.Description);
 }
}).addTo(map);


//LATLON->UTMK변환좌표 출력계
function locater(x_, y_) {
        this.x = x_;
        this.y = y_;
        this.ret = function() {
         return (new sop.LatLng(this.x, this.y));
        };
}

//INFOdatas의 구조체 배열
function INFER(ADDR_, WDDIR_) {
	this.ADDR = ADDR_;
	this.WDDIR = WDDIR_;
}

//정보를 받아 지도상에 최종 출력하는 함수
function mark(loc,info){
    for (let i = 0; i < loc.length; i++) {
		let content=
		"<div style='font-family: dotum, arial, sans-serif;font-size: 10px; font-weight: bold;margin-bottom: 5px;'> "+
		`${info[i].ADDR}`+ 
		"</div><table style='border-spacing: 2px; border: 0px'><tbody><tr><td style='color:#767676;padding-right:12px'>"+ 
		`${info[i].WDDIR}`+
		"</td></tr></tbody></table>";
        new sop.marker(sop.utmk(loc[i].x, loc[i].y)).addTo(map).bindInfoWindow(content).openInfoWindow();
    }    
}

//마커json처리
for (let i = 0; i < Object.keys(jsonData[0]).length; i++) {
	LOCdatas.push(new locater(parseFloat(jsonData[0][i].frfrSttmnLctnYcrd),parseFloat(jsonData[0][i].frfrSttmnLctnXcrd)).ret())
	INFOdatas.push(new INFER(jsonData[0][i].frfrSttmnAddr,jsonData[0][i].frfrOccrrWndrcCd))	
}
//heatMap json처리 반복문멈춰!!!
for (let i = 0; i < Object.keys(heatmapCoord.x).length; i++) {
	HeatCoordDatas.push(new locater(parseFloat(heatmapCoord.x[i]),parseFloat(heatmapCoord.y[i])).ret())
}
for (let i = 0; i < HeatCoordDatas.length; i++) {
	myHeatCoordDatas.push(new Array(HeatCoordDatas[i].x,HeatCoordDatas[i].y));
}

//마커표시함수호출
mark(LOCdatas,INFOdatas);

//히트맵최종표시단
var heat = sop.heatLayer(myHeatCoordDatas).addTo(map);
heat.setOptions({
	minOpacity : 0.5,
	radius : 20,
	blur : 10,
	max : 200,
});

</script>
	<script type="text/javascript" src="./js/jquery-3.2.1.min.js"></script>
	<script type="text/javascript" src="./js/ui.js"></script>
	<script data-cfasync="false" type="text/javascript" src="./js/form-submission-handler.js"></script>
	<script src="//cdnjs.cloudflare.com/ajax/libs/timepicker/1.3.5/jquery.timepicker.min.js"></script>
</body>
</html>