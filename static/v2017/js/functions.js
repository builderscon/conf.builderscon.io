$(document).ready(function() {

	// Smooth scroll
	$('a[href^="#top"]').click(function() {
		var speed = 400;
		var href= $(this).attr("href");
		var target = $(href == "#" || href == "" ? 'html' : href);
		var position = target.offset().top - 60;
		$('body,html').animate({scrollTop:position}, speed, 'swing');
		return false;
	});

	// Fade Link
/*	$('a, input[type="submit"], input[type="image"]').hover(function() {
		$(this).stop().fadeTo('slow', 0.5);
	},
	function() {
		$(this).stop().fadeTo('slow', 1);
	});*/

	// PAGE TOP
	$('#pagetop').hide();
	$(window).scroll(function () {
		if ($(this).scrollTop() > 100) {
			$('#pagetop').fadeIn();
		} else {
			$('#pagetop').fadeOut();
		}
	});

	// DropdownNavi
	$('.button-collapse').sideNav();

	// Multiple background
	$('.container section:nth-child(3n+1)').each(function(){
		$(this).addClass('section-first');
	})
	$('.container section:nth-child(3n+2)').each(function(){
		$(this).addClass('section-second');
	})
	$('.container section:nth-child(3n)').each(function(){
		$(this).addClass('section-third');
	})

	// Google Map
	$('.iframe').click(function(){
		$('.iframe iframe').css('pointer-events', 'auto');
	});

});

// RELAYOUT
var timer = false;
var windowSize = window.innerWidth ? window.innerWidth: $(window).width();
$(window).resize(function() {
	var ReWindowSize = window.innerWidth ? window.innerWidth: $(window).width();
//	alert(windowSize);
	if (windowSize >= 900) {
		
	}
	if (windowSize <= 899) {
		
	}
	if (timer !== false) {
		clearTimeout(timer);
	}
	if (windowSize != ReWindowSize) {
		location.href = location.href;
	}
});


