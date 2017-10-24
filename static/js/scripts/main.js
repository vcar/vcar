/*
 * Main JS application file :  app.js
 * =========================
 */

$(document).ready(function() {
    // Switch Theme -------------------------------------------------------------
    // if ($.cookie("dark-theme")) {
    //     $('body').removeClass("light").addClass("dark");
    //     $('#switch-mode').html('<i class="fa fa-sun-o"></i> Light mode');
    // } else {
    //     $('body').removeClass("dark").addClass("light");
    //     $('#switch-mode').html('<i class="fa fa-moon-o"></i> Dark mode');
    // }
    $('#switch-mode').click(function() {
        if ($.cookie("dark-theme")) {
            $.removeCookie("dark-theme", {
                path: '/'
            });
            $('#switch-mode').html('<i class="fa fa-moon-o"></i> Dark mode');
        } else {
            $.cookie("dark-theme", 1, {
                expires: 365,
                path: '/'
            });
            $('#switch-mode').html('<i class="fa fa-sun-o"></i> Light mode');
        }
        location.reload();
    });

    // Switch Sidebar ---------------------------------------------------------
    // if ($.cookie("sidebar-collapse")) {
    //     $('body').removeClass("light").addClass("dark");
    //     $('#switch-mode').html('<i class="fa fa-sun-o"></i> Light mode');
    // } else {
    //     $('body').removeClass("dark").addClass("light");
    //     $('#switch-mode').html('<i class="fa fa-moon-o"></i> Dark mode');
    // }
    $('#switch-sidebar').click(function() {
        if ($.cookie("sidebar-collapse")) {
            $.removeCookie("sidebar-collapse", {
                path: '/'
            });
            $('#switch-sidebar').html('<i class="fa fa-minus-square-o"></i> Collapse sidebar');
        } else {
            $.cookie("sidebar-collapse", 1, {
                expires: 365,
                path: '/'
            });
            $('#switch-sidebar').html('<i class="fa fa-plus-square-o"></i> Expand sidebar');
        }
        location.reload();
    });
});









var toastr = window.toastr;
toastr.options = {
    closeButton: false,
    closeEasing: 'swing',
    // showMethod: 'slideUp',
    closeMethod: 'slideDown',
    positionClass: 'toast-bottom-right',
    progressBar: false
};

/* turning flask flash messages into js popup notifications */

window.popupMessages.forEach(function(m, i) {
    var category = m[0];
    var text = m[1];
    setTimeout(function() {
        switch (category) {
            case 'success':
                toastr.success(text);
                break;
            case 'warning':
                toastr.warning(text);
                break;
            case 'error':
                toastr.error(text);
                break;
            default:
                toastr.info(text);
                break;
        }
    }, (1 + i) * 1500);
});

$(window).load(function() {

    $('.full').click(function(e) {
        console.log("Clicked");
        $('.vcar-box').toggleClass('fullscreen');
    });

});

$(function() {

    $('input').iCheck({
        checkboxClass: 'icheckbox_square-orange',
        radioClass: 'iradio_square-orange',
        increaseArea: '20%' // optional
    });

    // var iradio = $('.iradio_square-orange');
    // if(iradio.hasClass('.checked')){
    // 	iradio.closest('.btn-vcar').addClass('active');
    // }

    //Confirmation
    $('[data-toggle=confirmation]').confirmation({
        rootSelector: '[data-confirm=confirmation]',
    });

});
