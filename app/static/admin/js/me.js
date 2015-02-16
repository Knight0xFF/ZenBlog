jQuery(document).ready(function($){       
	$('.title a').hover(function() {         
	$(this).stop().animate({'marginLeft': '13px'}, 300);          
	}, function() {       
	$(this).stop().animate({'marginLeft': '0px'}, 300);          
	});
	
	$('#mainmenu ul li a').hover(function() {          
	$(this).stop().animate({'marginTop': '3px'}, 300);      
	}, function() {       
	$(this).stop().animate({'marginTop': '0px'}, 200);
	});
   
	$('.title a').click(function(e) {   
        e.preventDefault();   
        var htm = 'Loading',   
        i = 4,   
        t = $(this).html(htm).unbind('click'); (function ct() {   
            i < 0 ? (i = 4, t.html(htm), ct()) : (t[0].innerHTML += '.', i--, setTimeout(ct, 150))   
        })();   
        window.location = this.href   
    });   
});

$(document).ready(function(){
	//首先将#back-to-top隐藏
	$("#back-to-top").hide();
	//当滚动条的位置处于距顶部100像素以下时，跳转链接出现，否则消失
	$(function () {
		$(window).scroll(function(){
		if ($(window).scrollTop()>100){
		$("#back-to-top").fadeIn(1500);
		}
		else
		{
		$("#back-to-top").fadeOut(1500);
		}
		});
		//当点击跳转链接后，回到页面顶部位置
		$("#back-to-top").click(function(){
		$('body,html').animate({scrollTop:0},1000);
		return false;
		});
		});
		});


