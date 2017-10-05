// Import required modules
var gulp = require('gulp'),
    concat = require('gulp-concat'),
    rename = require('gulp-rename'),
    uglify = require('gulp-uglify'),
    cleanCSS = require('gulp-clean-css'),
    sourcemaps = require('gulp-sourcemaps'),
    watch = require('gulp-watch'),
    browserSync = require('browser-sync').create(),
    mode = require('gulp-mode')({modes: ["prod", "dev"], default: "dev"});

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
    'static/js/scripts/main.js',
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
        .pipe(sourcemaps.init())
        .pipe(mode.dev(concat('vendor.js')))
        .pipe(mode.prod(concat('vendor.min.js')))
        .pipe(mode.prod(uglify()))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(js_dist));
});

// Gulp vendor styles task ----------------------------------------------------
gulp.task('css_vendor', function() {
    return gulp.src(vendor_css_files)
        .pipe(sourcemaps.init())
        .pipe(mode.dev(concat('vendor.css')))
        .pipe(mode.prod(concat('vendor.min.css')))
        .pipe(mode.prod(cleanCSS()))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(css_dist));
});

// Gulp application scripts task ----------------------------------------------
gulp.task('js_app', function() {
    return gulp.src(app_js_files)
        .pipe(sourcemaps.init())
        .pipe(mode.dev(concat('app.js')))   
        .pipe(mode.prod(concat('app.min.js')))   
        .pipe(mode.prod(uglify()))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(js_dist));
});

// Gulp app styles task ----------------------------------------------------
gulp.task('css_app', function() {
    return gulp.src(app_css_files)
        .pipe(sourcemaps.init())
        .pipe(mode.dev(concat('app.css')))
        .pipe(mode.prod(concat('app.min.css')))
        .pipe(mode.prod(cleanCSS()))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(css_dist));
});

// Gulp frontend scripts task --------------------------------------------
gulp.task('js_front', function() {
    return gulp.src(front_js_files)
        .pipe(sourcemaps.init())
        .pipe(mode.dev(concat('frontend.js')))
        .pipe(mode.prod(concat('frontend.min.js')))
        .pipe(mode.prod(uglify()))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(js_dist));
});

// Gulp frontend styles task --------------------------------------------
gulp.task('css_front', function() {
    return gulp.src(front_css_files)
        .pipe(sourcemaps.init())
        .pipe(mode.dev(concat('frontend.css')))
        .pipe(mode.prod(concat('frontend.min.css')))
        .pipe(mode.prod(cleanCSS()))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(css_dist));
});

// Gulp group tasks ----------------------------------------------------------
gulp.task('default', ['css_app', 'js_app']);
gulp.task('vendor', ['css_vendor', 'js_vendor']);
gulp.task('front', ['css_front', 'js_front']);
gulp.task('js', ['js_app', 'js_front']);
gulp.task('css', ['css_app', 'css_front']);
gulp.task('build', ['css_vendor', 'js_vendor', 'css_app', 'js_app', 'css_front', 'js_front']);

// Gulp watch -----------------------------------------------------------------
gulp.task('watch', function (){
  gulp.watch('static/css/**/*.css', ['css']);
  gulp.watch('static/js/**/*.js', ['js']);
});
