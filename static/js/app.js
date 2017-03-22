/*! Flask-AdminLTE app.js
 * ======================
 * Main JS application file for Flask-AdminLTE v2. This file
 * should be included in all pages. It handles Flask-Admin
 * specific options and plugins.
 *
 * @Author  Justus Luthy
 * @Email   <justus@luthyenterprises.com>
 * @version 2.3.3
 * @license MIT <http://opensource.org/licenses/MIT>
 */

var toastr = window.toastr;
toastr.options = {
	closeButton: true,
	closeEasing: 'swing',
	closeMethod: 'slideUp',
	positionClass: 'toast-top-center',
	showMethod: 'slideDown',
	progressBar: true
};

/* turning flask flash messages into js popup notifications */
window.popupMessages.forEach(function(m, i) {
	var category = m[0] || 'success';
	var text = m[1];
	console.log(category);
	console.log(text);
	setTimeout(function() {
		toastr.info(text);
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

});
$(function() {

    var ul = $('#upload ul');
    var acceptFileTypes = /^(application\/json|text\/plain|text\/csv)$/i;
    var extensions = ['json', 'txt', 'csv'];

    $('#drop a').click(function() {
        $(this).parent().find('input').click();
    });

    // Initialize the jQuery File Upload plugin
    $('#upload').fileupload({

        dropZone: $('#drop'),

        add: function(e, data) {
            var uploadError = true;
            var re = /(?:\.([^.]+))?$/;
            var ext = re.exec(data.originalFiles[0]['name'])[1];
            // Check whether a file is accepted or not.
            if (data.originalFiles[0]['type'].length && acceptFileTypes.test(data.originalFiles[0]['type'])) {
                uploadError = false;
            } else if (data.originalFiles[0]['type'].length == 0 && ext != undefined && ext.length) {
                if (extensions.indexOf(ext) >= 0)
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
