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
