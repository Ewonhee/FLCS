// 메뉴 나타나기
$(function () {
  $(".menu1_dateTime").hide();
  $(".menu1").click(function () {
      $(".menu1_dateTime").show();
      /*
      $("#btn1").click(function () {
        $(".menu1_dateTime").hide();
      });
      */
  });
  
  // 외부 클릭 시 좌측 사이드 메뉴 숨기기
  $('.wrap').on('click', function () {
      $('.menu1_dateTime').fadeOut();
      $('.menu1').fadeIn();
  });

  $('.time').timepicker({
    datepicker:false,
    allowTimes:[
      '00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'
    ],
    language : 'ko', // 화면에 출력될 언어를 한국어로 설정한다.
    pickTime : false, // 사용자로부터 시간 선택을 허용하려면 true를 설정하거나 pickTime 옵션을 생략한다.
    defalutDate : new Date() // 기본값으로 오늘 날짜를 입력한다. 기본값을 해제하려면 defaultDate 옵션을 생략한다.
  });
  

  $(".menu4_dateTime").hide();
  $(".menu4").click(function () {
      $(".menu4_dateTime").toggle();
  });
  // 외부 클릭 시 좌측 사이드 메뉴 숨기기
  $('.overlay').on('click', function () {
      $('.menu4_dateTime').fadeOut();
      $('.menu4').fadeIn();
  });

/*
$(document).ready(function(){
  // menu 클래스 바로 하위에 있는 a 태그를 클릭했을때
  $(".menu1").click(function(){
      var submenu = $(this).next("ul");

      // submenu 가 화면상에 보일때는 위로 보드랍게 접고 아니면 아래로 보드랍게 펼치기
      if( submenu.is(":visible") ){
          submenu.slideUp();
      }else{
          submenu.slideDown();
      }
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
	//faq 게시판
	$(".accordio_box ol li").click(function(){
		$(".accordio_box ol li").removeClass("on");
		$(this).addClass("on");
	});
	$(".close").click(function(){
		$(".thankyou_message").css("display", "none");
	});
});

