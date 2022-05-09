// 메뉴 나타나기
$(function () {
  $(".menu1_dateTime").hide();
  $(".menu1").click(function () {
      $(".menu1_dateTime").fadeToggle();
  });
  
  // 외부 클릭 시 좌측 사이드 메뉴 숨기기
  $('.overlay').on('click', function () {
      $('.menu1_dateTime').fadeOut();
      $('.menu1').fadeIn();
  });


  $(".menu4_dateTime").hide();
  $(".menu4").click(function () {
      $(".menu4_dateTime").fadeToggle();
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

