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