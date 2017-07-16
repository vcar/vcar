/*
 * Main JS application file :  app.js
 * =========================
 */

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

window.popupMessages.forEach(function (m, i) {
    var category = m[0];
    var text = m[1];
    setTimeout(function () {
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

$(window).load(function () {

    $('.full').click(function (e) {
        console.log("Clicked");
        $('.vcar-box').toggleClass('fullscreen');
    });

});

$(function () {

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

$(function () {

    var ul = $('#upload ul');
    var acceptFileTypes = /^(application\/json|text\/plain|text\/csv)$/i;
    var extensions = ['json', 'txt', 'csv', 'xml', 'mat', 'zip'];

    $('#drop a').click(function () {
        $(this).parent().find('input').click();
    });

    // Initialize the jQuery File Upload plugin
    $('#upload').fileupload({

        dropZone: $('#drop'),

        add: function (e, data) {
            var uploadError = true;
            var re = /(?:\.([^.]+))?$/;
            var ext = re.exec(data.files[0]['name'])[1];
            // Check whether a file is accepted or not.

            if (ext != undefined && ext.length && (extensions.indexOf(ext) >= 0)) {
                uploadError = false;
            }
            if (!uploadError) {
                // if File Accepted :
                console.log('file accepted ');
                var tpl = $('<li class="working"><input type="text" value="0" data-width="48" data-height="48" data-fgColor="#0788a5" data-readOnly="1" data-bgColor="#3e4043" /><p></p><span></span></li>');
                tpl.find('p').text(data.files[0].name).append('<i>' + formatFileSize(data.files[0].size) + '</i>');
                data.context = tpl.appendTo(ul);
                tpl.find('input').knob({
                    fgColor: "#03A100"
                });

                tpl.find('span').click(function () {
                    if (tpl.hasClass('working')) {
                        jqXHR.abort();
                    }
                    tpl.fadeOut(function () {
                        tpl.remove();
                    });
                });
                var jqXHR = data.submit();
            } else {
                // if Error
                console.log('not working')
                var tpl = $('<li class="error working"><div class="bad-extension"></div><p></p><span></span></li>');
                tpl.find('p').text(data.files[0].name).append('<i>Extension not supported</i>');
                data.context = tpl.appendTo(ul);
                tpl.find('span').click(function () {
                    tpl.fadeOut(function () {
                        tpl.remove();
                    });
                });
            }
        },

        progress: function (e, data) {

            // Calculate the completion percentage of the upload
            var progress = parseInt(data.loaded / data.total * 100, 10);

            // Update the hidden input field and trigger a change
            // so that the jQuery knob plugin knows to update the dial
            data.context.find('input').val(progress).change();

            if (progress == 100) {
                data.context.removeClass('working');
            }
        },

        fail: function (e, data) {
            // Something has gone wrong!
            data.context.addClass('error');

        },

        done: function (e, data) {
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
    $(document).on('drop dragover', function (e) {
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

var well = $('.well-error');
if (well) {
    well.slideDown(1000)
        .delay(10000)
        .slideUp(500)
}
/*********************** Signal Page Form and validation ********************/

function display_error(msg, element) {
    errorDiv = document.getElementById('validation_errors');
    errorDiv.textContent = msg;
    element.classList.add('has-error');
    console.log(msg);
}

function make_validation_success(element) {
    element.classList.remove('has-error');
    errorDiv = document.getElementById('validation_errors');
    errorDiv.textContent = "";
}
/**
 * filter blank element from string array
 * @param arr string array
 * @returns {Array} array of string, all the strings are guarenteed to have a length bigger than 0
 */
function filter_blanks(arr) {
    ret = [];
    for (let element of arr) {
        if (element.length == 0) continue;
        ret.push(element);
    }
    return ret;
}


/**
 * check if the number of elments match the number specified in the input
 */
function start_elements_validation_listener() {
    let number_regex = /^([1-9][0-9]*)$/;
    let split_regex = /\s*\-\s*/;
    let numberOfValues = document.getElementById('number');
    let values = document.getElementById('values');

    numberOfValues.onkeyup = function (e) {
        let cur = numberOfValues.value;
        let valid = true;
        if (!number_regex.test(cur)) {
            valid = false;
            display_error("The number of tokens must be a number", numberOfValues.parentElement);
        } else {
            let actualNumber = parseInt(cur);
            let values = document.getElementById('values');
            let actualValues = values.value.split(split_regex);
            console.log(actualValues);
            if (actualValues.length != actualNumber) {
                valid = false;
                let diff = actualNumber - actualValues.length;
                if (actualValues.length == 0) diff += 1; // count empty string as one, must be substracted
                if (diff > 0) {
                    display_error("the number of tokens is smaller then declared, " + diff + " needed !", values.parentElement);
                } else {
                    display_error("the number of tokens is bigger then declared, " + (-diff) + " must be removed !", values.parentElement);
                }
            }
            if (valid) {
                make_validation_success(numberOfValues.parentNode);
            }
        }
    }

    values.onkeyup = function (e) {
        if (numberOfValues.value) {
            let number = parseInt(numberOfValues.value);
            let valid = true;
            let actualValues = filter_blanks(values.value.split(split_regex));
            if (actualValues.length != number) {
                valid = false;
                console.log('actual values ', actualValues, ' actual values length ', actualValues.length)
                let diff = number - actualValues.length;
                if (actualValues.length == 0) diff += 1; // count empty string as one, must be substracted
                if (diff > 0) {
                    display_error("the number of tokens is smaller then declared, " + diff + " needed !", values.parentElement);
                } else {
                    display_error("the number of tokens is bigger then declared, " + (-diff) + " must be removed !", values.parentElement);
                }
            }
            if (valid) {
                make_validation_success(values.parentNode);
            }
        }
    }
}

/**
 * min and max validation checkers
 */
function start_number_validation_listener() {
    let minValue = document.getElementById('min-value');
    let maxValue = document.getElementById('max-value');
    let number_regex = /^([1-9][0-9]*)$/;

    minValue.onkeyup = function (e) {
        let cur = minValue.value;
        let actualValue = parseInt(cur);
        let valid = true;
        if (!number_regex.test(cur)) {
            valid = false;
            display_error("The Value must be a number", minValue.parentElement);
        } else {
            if (maxValue.value && parseInt(maxValue.value) < actualValue) {
                valid = false;
                display_error("the value must be smaller than the max  value", minValue);
            }
        }
        if (valid) {
            make_validation_success(minValue.parentNode);
        }
    }

    maxValue.onkeyup = function (e) {
        let cur = maxValue.value;
        let actualValue = parseInt(cur);
        let valid = true;
        if (!number_regex.test(cur)) {
            valid = false;
            display_error("The Value must be a number", maxValue.parentElement);
        } else {
            if (minValue.value && parseInt(minValue.value) > actualValue) {
                valid = false;
                display_error("the value must be bigger than the min value", maxValue.parentElement);
            }
        }
        if (valid) {
            make_validation_success(maxValue.parentElement);
        }
    }
}

var type = document.getElementById('type');
if (type) {
    var value = type.selectedOptions[0].value;
    if (value === "Numerical") {
        $('#_added').remove()
        $('#validation_errors').remove()
        $(type.parentElement).after('<div id="_added" class="form-group"><input type="text" class="form-control" name="min_value" id="min-value" placeholder="minimum value"><input type="text" id="max-value" class="form-control" name="max_value" placeholder="maximum value"></div><div id="validation_errors"></div>');
        start_number_validation_listener();
    } else if (value == "States") {
        $('#_added').remove()
        $('#validation_errors').remove()
        $(type.parentElement).after('<div id="_added" class="form-group"> <input type="text" class="form-control" id="number" name="number" placeholder="Number of states"><input type="text" class="form-control" id="values" name="values" placeholder="Example: A - B - C "></div><div id="validation_errors"></div>');
        start_elements_validation_listener();
    } else {
        $('#_added').slideUp(300, function () {
            $('#_added').remove()
        })
    }

    type.onchange = function (e) {
        var value = type.selectedOptions[0].value;
        if (value === "Numerical") {
            $('#_added').remove()
            $('#validation_errors').remove()
            $(type.parentElement).after('<div id="_added" class="form-group"><input type="text" class="form-control" name="min_value" id="min-value" placeholder="minimum value"><input type="text" id="max-value" class="form-control" name="max_value" placeholder="maximum value"></div><div id="validation_errors"></div>');
            start_number_validation_listener();
        } else if (value == "States") {
            $('#_added').remove()
            $('#validation_errors').remove()
            $(type.parentElement).after('<div id="_added" class="form-group"> <input type="text" class="form-control" id="number" name="number" placeholder="Number of states"><input type="text" class="form-control" id="values" name="values" placeholder="Example: A - B - C "></div><div id="validation_errors"></div>');
            start_elements_validation_listener();
        } else {
            $('#_added').slideUp(300, function () {
                $('#_added').remove()
            })
        }
    }
}


/*--------------------------- Signals File Upload -------------------------------*/

let dropZone = document.querySelector('.drop-file');
let fileInput = document.querySelector('input[type*=file]');
let fileInfo = document.querySelector('#file-info');

if (dropZone) {

    dropZone.addEventListener('click', function (e) {
        fileInput.click();
    })

    fileInput.onchange = function () {
        if (fileInput.files[0].name.endsWith(".csv")) {
            fileInfo.textContent = "1 File Chosen " + fileInput.files[0].name;
            fileInfo.className = '';
        } else {
            fileInfo.textContent = "Please make sure that the File is a csv file";
        }
    }

    dropZone.ondragover = function () {
        this.className = 'drop-file drop-on';
        return false;
    }

    dropZone.ondragleave = function () {
        this.className = 'drop-file';
        return false;
    }

    dropZone.ondrop = function (e) {
        e.preventDefault();
        this.className = 'drop-file';
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            if (e.dataTransfer.files[0].name.endsWith(".csv")) {
                fileInput.files = e.dataTransfer.files;
                fileInfo.textContent = "1 File Chosen " + e.dataTransfer.files[0].name;
                fileInfo.className = '';
            } else {
                fileInfo.textContent = "Please make sure that the File is a csv file";
            }
        }
    }

}