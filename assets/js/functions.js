function include(scriptUrl) {
	document.write('<script src="' + scriptUrl + '"></script>');
}

include('/assets/js/jquery.cookie.js');
include('/assets/js/jquery.easing.1.3.js');
include('/assets/js/jquery.rotate.js');

(function ($) {
	var windowSize = window.innerWidth ? window.innerWidth: $(window).width();
	var maxWidth = 900;
	if (windowSize <= 899) {
		include('./assets/js/jquery.mmenu.all.min.js');
		$(document).ready(function () {
			$('nav#menu').mmenu({
				offCanvas: {
					pageSelector: '#wrapper',
					position: 'right'
				},
				navbar: {
					title: 'builderscon'
				},
				extensions: ['pagedim-black', 'pageshadow', 'theme-white'],
				autoHeight: true,
				dragOpen: {
					open: 'true'
				}
			});
		});
	}
})(jQuery);

$(function() {
//$(document).ready(function() {

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
	$('a, input[type="submit"], input[type="image"]').hover(function() {
		$(this).stop().fadeTo('slow', 0.5);
	},
	function() {
		$(this).stop().fadeTo('slow', 1);
	});

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
	$('#menu li').hover(function(){
		$('ul:not(:animated)', this).slideDown('fast');
	}, function(){
		$('ul.dropdown',this).slideUp('fast');
	});

	// IMGCLOCK
	analog_clock();

	// OPENING ANIMATION
	setTimeout(function() {
		$('#hexlogo').fadeIn('1800');
		return false;
	},800);
	$(window).load(function(){
		$.cookie('BUIDERCONIMG', 'access', { path: '/', expires: 1 });
	});
	if(!$.cookie("BUIDERCONIMG")){ LodingAnimation(); }
//	LodingAnimation();

});

// RELAYOUT
var timer = false;
var windowSize = window.innerWidth ? window.innerWidth: $(window).width();
$(window).resize(function() {

	// IMGCLOCK
	analog_clock();

	var ReWindowSize = window.innerWidth ? window.innerWidth: $(window).width();
//	alert(windowSize);
	if (windowSize >= 900) {
		
	}
	if (windowSize <= 899) {
		
	}
	if (timer !== false) {
		clearTimeout(timer);
	}
/*	timer = setTimeout(function() {
//		console.log('resized');
		location.href = location.href;
	}, 200);*/
	if (windowSize != ReWindowSize) {
		location.href = location.href;
	}

});

// OPENING ANIMATION
function LodingAnimation() {
	var windowSize = window.innerWidth ? window.innerWidth: $(window).width();
	var maxWidth = 900;
	if (windowSize < maxWidth) {
		$(window).load(function() {
			$('#hexlogo .base').css({ top: '50%', left: '50%', width: '0px', height: '0px', margin: '0 0 0 0', display: 'none' });
			$('#hexlogo .logo').css({ top: '50%', left: '50%', width: '0px', height: '0px', margin: '0 0 0 0', display: 'none' });
			setTimeout(function() {
				$('#hexlogo .base').show().stop().animate({ top: '50%', left: '50%', width: '240px', height: '240px', margin: '-120px 0 0 -120px', opacity: '0.85' }, 1800, 'easeOutElastic');
				return false;
			},1600);
			setTimeout(function() {
				$('#hexlogo .logo').show().stop().animate({ top: '50%', left: '50%', width: '140px', height: '140px', margin: '-70px 0 0 -70px' }, 1800, 'easeOutElastic');
				return false;
			},1800);
		});
	} else {
		$(window).load(function() {
			$('#hexlogo .base').css({ top: '50%', left: '50%', width: '0px', height: '0px', margin: '0 0 0 0', display: 'none' });
			$('#hexlogo .logo').css({ top: '50%', left: '50%', width: '0px', height: '0px', margin: '0 0 0 0', display: 'none' });
			setTimeout(function() {
				$('#hexlogo .base').show().stop().animate({ top: '50%', left: '50%', width: '310px', height: '310px', margin: '-155px 0 0 -155px', opacity: '0.85' }, 1800, 'easeOutElastic');
				return false;
			},1600);
			setTimeout(function() {
				$('#hexlogo .logo').show().stop().animate({ top: '50%', left: '50%', width: '180px', height: '180px', margin: '-90px 0 0 -90px' }, 1800, 'easeOutElastic');
				return false;
			},1800);
		});
	}
}

// IMGCLOCK
function analog_clock(){
	today = new Date();
	var hour = today.getHours();
	var minute = today.getMinutes();
	var second = today.getSeconds();
//	$('#hexlogo .base img').rotate(hour*30+minute/2);
	$('#hexlogo .logo img').rotate(minute*6+second/10);
	$('#hexlogo .base img').rotate(second*6);
	setTimeout("analog_clock()",1000);
}




