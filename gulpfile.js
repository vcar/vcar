
var gulp = require('gulp');
var concatJs = require('gulp-concat');
var concatCss = require('gulp-concat-css');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var cleanCSS = require('gulp-clean-css');

// ToDo : add gulp watch when needed

// Static files =============================================================== 

// Global Directories

var css_dist = 'static/css/';
var js_dist = 'static/js/';

// Vendor files
var vendor_css_files = [
    'static/vendor/bootstrap/bootstrap.css',
    'static/vendor/adminlte/adminlte.css',
    'static/vendor/font-awesome/font-awesome.css',
    'static/vendor/toastr/toastr.css',
    'static/vendor/pace/pace.css',
    'static/vendor/icheck/icheck.css',
    'static/vendor/vis/vis.min.css',
];

var vendor_js_files = [
    'static/vendor/jquery/*.js',
    'static/vendor/jqueryui/*.js',
    'static/vendor/bootstrap/*.js',
    'static/vendor/confirmation/*.js',
    'static/vendor/toastr/*.js',
    'static/vendor/pace/*.js',
    'static/vendor/slimscroll/*.js',
    'static/vendor/fastclick/*.js',
    'static/vendor/icheck/*.js',
    'static/vendor/vis/vis.min.js',
    'static/vendor/fileupload/fileupload.js',
    'static/vendor/fileupload/fileupload-process.js',
    'static/vendor/fileupload/fileupload-validate.js',
    'static/vendor/conditionize/conditionize.jquery.js',
    'static/vendor/knob/*.js',
    'static/vendor/adminlte/*.js'
];

// Application files
var app_css_files = [
    'static/css/styles/global.css',
    'static/css/skins/skin-vcar_blue.css',
    'static/css/styles/uploader.css',
];

var app_js_files = [
    'static/js/scripts/app.js',
    'static/js/scripts/uploader.js',
];

// FrontEnd files
var front_css_files = [
    'static/vendor/bootstrap/bootstrap.css',
    'static/vendor/font-awesome/font-awesome.css',
    'static/vendor/ionicons/ionicons.css',
    'static/vendor/animate/animate.css',
    'static/css/styles/frontend.css',
];

var front_js_files = [
    'static/vendor/jquery/jquery.js',
    'static/vendor/bootstrap/bootstrap.js',
    'static/vendor/waypoints/jquery.waypoints.js',
    'static/vendor/parallax/jquery.parallax.js',
    'static/vendor/sticky/jquery.sticky.js',
    'static/vendor/smoothscroll/smoothscroll.js',
    'static/vendor/backstretch/backstretch.js',
    'static/js/scripts/frontend.js',
];

// End static files ===========================================================

// Gulp vendor scripts task ---------------------------------------------------

gulp.task('js_vendor', function() {
    return gulp.src(vendor_js_files)
        .pipe(concatJs('vendor.js'))
        .pipe(gulp.dest(js_dist))
        .pipe(uglify())
        .pipe(concatJs('vendor.min.js'))
        .pipe(gulp.dest(js_dist));
});

// Gulp application scripts task ----------------------------------------------

gulp.task('js_app', function() {
    return gulp.src(app_js_files)
        .pipe(concatJs('app.js'))
        .pipe(gulp.dest(js_dist))
        .pipe(uglify())
        .pipe(concatJs('app.min.js'))
        .pipe(gulp.dest(js_dist));
});

// Gulp vendor styles task ----------------------------------------------------

gulp.task('css_vendor', function() {
    return gulp.src(vendor_css_files)
        .pipe(concatCss('vendor.css'))
        .pipe(gulp.dest(css_dist))
        .pipe(cleanCSS())
        .pipe(concatCss('vendor.min.css'))
        .pipe(gulp.dest(css_dist));
});

// Gulp app styles task ----------------------------------------------------

gulp.task('css_app', function() {
    return gulp.src(app_css_files)
        .pipe(concatCss('app.css'))
        .pipe(gulp.dest(css_dist))
        .pipe(cleanCSS())
        .pipe(concatCss('app.min.css'))
        .pipe(gulp.dest(css_dist));
});

// Gulp frontend scripts task --------------------------------------------

gulp.task('js_front', function() {
    return gulp.src(front_js_files)
        .pipe(concatJs('frontend.js'))
        .pipe(gulp.dest(js_dist))
        .pipe(cleanCSS())
        .pipe(concatJs('frontend.min.js'))
        .pipe(gulp.dest(js_dist));
});

// Gulp frontend styles task --------------------------------------------

gulp.task('css_front', function() {
    return gulp.src(front_css_files)
        .pipe(concatCss('frontend.css'))
        .pipe(gulp.dest(css_dist))
        .pipe(cleanCSS())
        .pipe(concatCss('frontend.min.css'))
        .pipe(gulp.dest(css_dist));
});

// Gulp group tasks ----------------------------------------------------------

gulp.task('default', ['css_app', 'js_app']);
gulp.task('vendor', ['css_vendor', 'js_vendor']);
gulp.task('front', ['css_front', 'js_front']);
gulp.task('all', ['css_vendor', 'js_vendor', 'css_app', 'js_app', 'css_front', 'js_front']);
