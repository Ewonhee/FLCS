<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<%@ include file="dbconn.jsp"%>

<%
	String sCondition2 = request.getParameter("ddate");
	String sCondition3 = request.getParameter("dtime");
	String sConditiontemp = null;
	if (sCondition3 != null)
		sConditiontemp = sCondition3.substring(0, sCondition3.length() - 3);

	if (sCondition2 == null)
		sCondition2 = "22-04-11";
	if (sCondition3 == null)
		sCondition3 = "12";
	if (sConditiontemp == null)
		sConditiontemp = "12";
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

	try {
		String sql_prop = "SELECT * FROM crdnttable WHERE DataCrawlingTime = \"" + sCondition2 + " " + sConditiontemp
		+ "\"";
		String sql_coor = "SELECT Coordinates FROM crdnttable WHERE DataCrawlingTime = \"" + sCondition2 + " "
		+ sConditiontemp + "\"";
		String sql_count_date = "SELECT COUNT(*) FROM crdnttable WHERE DataCrawlingTime = \"" + sCondition2 + " "
		+ sConditiontemp + "\"";
		pstmt1 = conn.prepareStatement(sql_prop);
		pstmt2 = conn.prepareStatement(sql_coor);
		pstmt3 = conn.prepareStatement(sql_count_date);
		rs1 = pstmt1.executeQuery();
		rs2 = pstmt2.executeQuery();
		rs3 = pstmt3.executeQuery();

		rs3.next();
		String num_data = rs3.getString("COUNT(*)");
		for (int i = 0; i < Integer.parseInt(num_data); i++) {
			rs1.next();
			String temp = rs1.getString("Properties");
			String temp2 = rs1.getString("Coordinates");
			sb1.append("{ \"type\": \"Feature\", \"properties\": { \"Description\": \"" + temp + "\"},");
			sb1.append("\"geometry\": { \"type\": \"Polygon\", \"coordinates\": " + temp2 + "} },");
		}
	} catch (SQLException ex) {
		out.println("테이블 호출 실패");
		out.println("SQL Exception : " + ex.getMessage());
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
	<%
		out.println("========================================산불의 진행 시간 : " + sCondition2 + " " + sCondition3 + "========================================");
		out.println("\n");
		%>
		<br>
		<br>
		<%
		out.println(sb1);
	%>