function setupMmenu() {
    // We need to clone nav#menu in order to allow
    // going back and forth between width >= maxWidth and width < maxWidth
    var cl = $('nav#menu').clone();
    cl.mmenu({
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
    $('nav#menu').append(cl);
}

function setupSmoothScrollToTop() {
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
}

function setupClock() {
    var h = $("#hexlogo");
    if (h == null) {
        return
    }

    // OPENING ANIMATION
    setTimeout(function() {
        h.fadeIn(1800);
        return false;
    },800);

    // only do the boing-boing once per day
    $(window).load(function(){
        $.cookie('BUILDERSCON_IMG', 'access', { path: '/', expires: 1 });
    });
    if(!$.cookie("BUILDERSCON_IMG")){ doBoingBoing(); }

    var turnclock;
    turnclock = function () {
        t = new Date();
        var hour = t.getHours();
        var minute = t.getMinutes();
        var second = t.getSeconds();
        $('.logo img', h).rotate(minute*6+second/10);
        $('.base img', h).rotate(second*6);
        setTimeout(turnclock,1000);
    };
    turnclock();
}

function setupDropdown() {
    $('#menu li').hover(
        function(){
            $('ul:not(:animated)', this).slideDown('fast');
        },
        function(){
            $('ul.dropdown',this).slideUp('fast');
	}
    );
}

$(document).ready(function() {
    setupMmenu()
    setupSmoothScrollToTop();
    setupClock();
    setupDropdown();
});

// RELAYOUT
var timer = false;
var windowSize = window.innerWidth ? window.innerWidth: $(window).width();
$(window).resize(function() {
	if (timer !== false) {
		clearTimeout(timer);
	}
});

// OPENING ANIMATION
function doBoingBoing() {
    var h = $("#hexlogo")
    if (h == null) {
        return
    }

    var windowSize = window.innerWidth ? window.innerWidth: $(window).width();
    var maxWidth = 900;

    var width0 = '310px';
    var width1 = '180px';
    var height0 = '310px';
    var height1 = '180px';
    var margin0 = '-155px 0 0 -155px';
    var margin1 = '-90px 0 0 -90px';

    if (windowSize < maxWidth) {
        width0 = '240px';
        width1 = '140px';
        height0 = '240px';
        height1 = '140px';
        margin0 = '-120px 0 0 -120px';
        margin1 = '-70px 0 0 -70px';
    }

    $('.base', h).css({ top: '50%', left: '50%', width: '0px', height: '0px', margin: '0 0 0 0', display: 'none' });
    $('.logo', h).css({ top: '50%', left: '50%', width: '0px', height: '0px', margin: '0 0 0 0', display: 'none' });
    setTimeout(function() {
        $('.base', h)
            .show()
            .stop()
            .animate({ top: '50%', left: '50%', width: width0, height: height0, margin: margin0, opacity: '0.85' }, 1800, 'easeOutElastic');
        return false;
    }, 1600);
    setTimeout(function() {
        $('.logo', h)
            .show()
            .stop()
            .animate({ top: '50%', left: '50%', width: width1, height: height1, margin: margin1}, 1800, 'easeOutElastic');
        return false;
    },1800);
}

