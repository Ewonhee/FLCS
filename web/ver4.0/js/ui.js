// 메뉴 나타나기
$(function () {
  /*
  $('#date').datetimepicker({
    datepicker:false,
    allowTimes:[
      '00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'
    ],
    language : 'ko', // 화면에 출력될 언어를 한국어로 설정한다.
  });*/

	//로고 클릭 시
	$(".logo_box").click(function(){
		$("nav ui").removeClass("on");
		$(".content").removeClass("prev this next");
		$("#container").css("max-width", "1200px");
	});
	
	//ajax 사용하기
	$(".book_roll li").click(function(){
		var _this =$(this);
		var liurl =_this.data("url");
		$(".notebook").html();
		$.ajax({
			type : 'post', //HTTP 요청 방식
			url : liurl, //해당 url
			dataType : 'html', //data 타입
			success : function(data) { //HTTP 요청 성공 후 데이터 전송
				$(".notebook").html(data);
			}
		});
	});
});
