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

$(function() {

    var ul = $('#upload ul');
    var acceptFileTypes = /^(application\/json|text\/plain|text\/csv)$/i;
    var extensions = ['json', 'txt', 'csv', 'xml', 'mat', 'zip'];

    $('#drop a').click(function() {
        $(this).parent().find('input').click();
    });

    // Initialize the jQuery File Upload plugin
    $('#upload').fileupload({

        dropZone: $('#drop'),

        add: function(e, data) {
            var uploadError = true;
            var re = /(?:\.([^.]+))?$/;
            var ext = re.exec(data.files[0]['name'])[1];
            // Check whether a file is accepted or not.

            if (ext != undefined && ext.length && (extensions.indexOf(ext) >= 0)) {
                uploadError = false;
            }
            if (!uploadError) {
                // if File Accepted :
                var tpl = $('<li class="working"><input type="text" value="0" data-width="48" data-height="48" data-fgColor="#0788a5" data-readOnly="1" data-bgColor="#3e4043" /><p></p><span></span></li>');
                tpl.find('p').text(data.files[0].name).append('<i>' + formatFileSize(data.files[0].size) + '</i>');
                data.context = tpl.appendTo(ul);
                tpl.find('input').knob({
                    fgColor: "#03A100"
                });

                tpl.find('span').click(function() {
                    if (tpl.hasClass('working')) {
                        jqXHR.abort();
                    }
                    tpl.fadeOut(function() {
                        tpl.remove();
                    });
                });
                var jqXHR = data.submit();
            } else {
                // if Error
                var tpl = $('<li class="error working"><div class="bad-extension"></div><p></p><span></span></li>');
                tpl.find('p').text(data.files[0].name).append('<i>Extension not supported</i>');
                data.context = tpl.appendTo(ul);
                tpl.find('span').click(function() {
                    tpl.fadeOut(function() {
                        tpl.remove();
                    });
                });
            }
        },

        progress: function(e, data) {

            // Calculate the completion percentage of the upload
            var progress = parseInt(data.loaded / data.total * 100, 10);

            // Update the hidden input field and trigger a change
            // so that the jQuery knob plugin knows to update the dial
            data.context.find('input').val(progress).change();

            if (progress == 100) {
                data.context.removeClass('working');
            }
        },

        fail: function(e, data) {
            // Something has gone wrong!
            data.context.addClass('error');

        },

        done: function(e, data) {
            var result = JSON.parse(data.result);
            if (result.status) {
                $('#send_files').append('<input type="hidden" name="files" value="' + result.message + '" />');
            } else {
                data.context.addClass('error');
                data.context.find('p').find('i').html(" " + result.message).addClass('fa fa-exclamation-circle');
            }
        }

    });

    // Prevent the default action when a file is dropped on the window
    $(document).on('drop dragover', function(e) {
        e.preventDefault();
    });

    // Helper function that formats the file sizes
    function formatFileSize(bytes) {
        if (typeof bytes !== 'number') {
            return '';
        }

        if (bytes >= 1000000000) {
            return (bytes / 1000000000).toFixed(2) + ' GB';
        }

        if (bytes >= 1000000) {
            return (bytes / 1000000).toFixed(2) + ' MB';
        }

        return (bytes / 1000).toFixed(2) + ' KB';
    }

});

//# sourceMappingURL=app.js.map
