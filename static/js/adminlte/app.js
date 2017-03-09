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
		switch(category){
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

});
