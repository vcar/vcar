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
var css_dist = 'core/dashboard/static/css/';
var js_dist = 'core/dashboard/static/js/';

// Vendor files
var vendor_css_files = [
    'core/dashboard/static/vendor/bootstrap/bootstrap.css',
    'core/dashboard/static/vendor/adminlte/adminlte.css',
    'core/dashboard/static/vendor/font-awesome/font-awesome.css',
    'core/dashboard/static/vendor/toastr/toastr.css',
    'core/dashboard/static/vendor/pace/pace.css',
    'core/dashboard/static/vendor/icheck/icheck.css',
    'core/dashboard/static/vendor/vis/vis.min.css',
];
var vendor_js_files = [
    'core/dashboard/static/vendor/jquery/*.js',
    'core/dashboard/static/vendor/jqueryui/*.js',
    'core/dashboard/static/vendor/bootstrap/*.js',
    'core/dashboard/static/vendor/confirmation/*.js',
    'core/dashboard/static/vendor/toastr/*.js',
    'core/dashboard/static/vendor/pace/*.js',
    'core/dashboard/static/vendor/slimscroll/*.js',
    'core/dashboard/static/vendor/fastclick/*.js',
    'core/dashboard/static/vendor/icheck/*.js',
    'core/dashboard/static/vendor/vis/vis.min.js',
    'core/dashboard/static/vendor/cookie/jquery.cookie.js',
    'core/dashboard/static/vendor/fileupload/fileupload.js',
    'core/dashboard/static/vendor/fileupload/fileupload-process.js',
    'core/dashboard/static/vendor/fileupload/fileupload-validate.js',
    'core/dashboard/static/vendor/conditionize/conditionize.jquery.js',
    'core/dashboard/static/vendor/knob/*.js',
    'core/dashboard/static/vendor/adminlte/*.js'
];

// Application files
var app_css_files = [
    'core/dashboard/static/css/styles/application.css',
    'core/dashboard/static/css/skins/dark-theme.css',
    'core/dashboard/static/css/skins/light-theme.css',
    'core/dashboard/static/css/components/**/*.css',
];
var app_js_files = [
    'core/dashboard/static/js/scripts/main.js',
    'core/dashboard/static/js/scripts/uploader.js',
];

// FrontEnd files
var front_css_files = [
    'core/dashboard/static/vendor/bootstrap/bootstrap.css',
    'core/dashboard/static/vendor/font-awesome/font-awesome.css',
    'core/dashboard/static/vendor/ionicons/ionicons.css',
    'core/dashboard/static/vendor/animate/animate.css',
    'core/dashboard/static/css/styles/frontend.css',
];
var front_js_files = [
    'core/dashboard/static/vendor/jquery/jquery.js',
    'core/dashboard/static/vendor/bootstrap/bootstrap.js',
    'core/dashboard/static/vendor/waypoints/jquery.waypoints.js',
    'core/dashboard/static/vendor/parallax/jquery.parallax.js',
    'core/dashboard/static/vendor/sticky/jquery.sticky.js',
    'core/dashboard/static/vendor/smoothscroll/smoothscroll.js',
    'core/dashboard/static/vendor/backstretch/backstretch.js',
    'core/dashboard/static/js/scripts/frontend.js',
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
  gulp.watch('core/dashboard/static/css/**/*.css', ['css']);
  gulp.watch('core/dashboard/static/js/**/*.js', ['js']);
});
