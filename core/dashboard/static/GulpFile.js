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
var css_dist = 'css/';
var js_dist = 'js/';

// Vendor files
var vendor_css_files = [
    'vendor/bootstrap/bootstrap.css',
    'vendor/adminlte/adminlte.css',
    'vendor/font-awesome/font-awesome.css',
    'vendor/toastr/toastr.css',
    'vendor/pace/pace.css',
    'vendor/icheck/icheck.css',
    'vendor/vis/vis.min.css',
];
var vendor_js_files = [
    'vendor/jquery/*.js',
    'vendor/jqueryui/*.js',
    'vendor/bootstrap/*.js',
    'vendor/confirmation/*.js',
    'vendor/toastr/*.js',
    'vendor/pace/*.js',
    'vendor/slimscroll/*.js',
    'vendor/fastclick/*.js',
    'vendor/icheck/*.js',
    'vendor/vis/vis.min.js',
    'vendor/cookie/jquery.cookie.js',
    'vendor/fileupload/fileupload.js',
    'vendor/fileupload/fileupload-process.js',
    'vendor/fileupload/fileupload-validate.js',
    'vendor/conditionize/conditionize.jquery.js',
    'vendor/knob/*.js',
    'vendor/adminlte/*.js'
];

// Application files
var app_css_files = [
    'css/styles/application.css',
    'css/skins/dark-theme.css',
    'css/skins/light-theme.css',
    'css/components/**/*.css',
];
var app_js_files = [
    'js/scripts/main.js',
    'js/scripts/uploader.js',
];

// FrontEnd files
var front_css_files = [
    'vendor/bootstrap/bootstrap.css',
    'vendor/font-awesome/font-awesome.css',
    'vendor/ionicons/ionicons.css',
    'vendor/animate/animate.css',
    'css/styles/frontend.css',
];
var front_js_files = [
    'vendor/jquery/jquery.js',
    'vendor/bootstrap/bootstrap.js',
    'vendor/waypoints/jquery.waypoints.js',
    'vendor/parallax/jquery.parallax.js',
    'vendor/sticky/jquery.sticky.js',
    'vendor/smoothscroll/smoothscroll.js',
    'vendor/backstretch/backstretch.js',
    'js/scripts/frontend.js',
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
  gulp.watch('css/**/*.css', ['css']);
  gulp.watch('js/**/*.js', ['js']);
});
