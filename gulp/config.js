'use strict';

var fs = require( 'fs' );
var paths = require( '../config/environment' ).paths;
var globAll = require( 'glob-all' );

module.exports = {
  pkg:    JSON.parse( fs.readFileSync( 'bower.json' ) ), // eslint-disable-line no-sync, no-inline-comments, max-len
  banner:
      '/*!\n' +
      ' *               ad$$               $$\n' +
      ' *              d$"                 $$\n' +
      ' *              $$                  $$\n' +
      ' *   ,adPYba.   $$$$$  $$.,dPYba.   $$.,dPYba.\n' +
      ' *  aP\'    `$:  $$     $$P\'    `$a  $$P\'    `$a\n' +
      ' *  $(          $$     $$(      )$  $$(      )$\n' +
      ' *  "b.    ,$:  $$     $$b.    ,$"  $$b.    ,$"\n' +
      ' *   `"Ybd$"\'   $$     $$`"YbdP"\'   $$`"YbdP"\'\n' +
      ' *                     $$\n' +
      ' *                     $$\n' +
      ' *                     $$\n' +
      ' *\n' +
      ' *  <%= pkg.name %> - v<%= pkg.version %>\n' +
      ' *  <%= pkg.homepage %>\n' +
      ' *  A public domain work of the Consumer Financial Protection Bureau\n' +
      ' */\n',
  lint: {
    src: [ paths.unprocessed + '/js/**/*.js' ],
    test:  [
      paths.test + '/unit_tests/**/*.js',
      paths.test + '/browser_tests/**/*.js'
    ],
    build: [
      'config/**/*.js',
      'gulpfile.js',
      'gulp/**/*.js'
    ]
  },
  test: {
    src:   paths.unprocessed + '/js/**/*.js',
    tests: paths.test
  },
  clean: {
    dest: paths.processed
  },
  scripts: {
    src: paths.unprocessed + '/js/**/*.js'
  },
  styles: {
    cwd:      paths.unprocessed + '/css',
    src:      '/main.less',
    dest:     paths.processed + '/css',
    settings: {
      paths:  globAll.sync( [
        paths.modules + '/capital-framework/**',
        paths.lib
      ] ),
      compress: true
    }
  },
  legacy: {
    cwd: paths.legacy,
    dest: paths.processed,
    scripts: [
      paths.legacy + '/nemo/_/js/jquery-1.5.1.min.js',
      paths.legacy + '/nemo/_/js/jquery.easing.1.3.js',
      paths.legacy + '/nemo/_/js/jquery.fitvids.min.js',
      paths.legacy + '/nemo/_/js/appendAround.js',
      paths.legacy + '/nemo/_/js/plugins.js',
      paths.legacy + '/nemo/_/js/main.js',
      paths.legacy + '/nemo/_/js/jquery.youtube-find-and-track.js',
      paths.legacy + '/nemo/_/js/AnalyticsTarget.js',
      paths.legacy + '/nemo/_/js/analytics-es.js'
    ]
  },
  images: {
    src:  paths.unprocessed + '/img/**',
    dest: paths.processed + '/img'
  },
  copy: {
    icons: {
      src:  paths.modules + '/capital-framework/src/cf-icons/src/fonts/*',
      dest: paths.processed + '/fonts/'
    },
    vendorFonts: {
      src:  paths.unprocessed + '/fonts/pdfreactor/*',
      dest: paths.processed + '/fonts/pdfreactor'
    },
    vendorCss: {
      src: [
        paths.lib + '/slick-carousel/slick/slick.css',
        paths.lib + '/slick-carousel/slick/slick.css.map',
        paths.unprocessed + '/css/pdfreactor-fonts.css'
      ],
      dest: paths.processed + '/css'
    },
    vendorImg: {
      src: [
        paths.lib + '/slick-carousel/slick/ajax-loader.gif'
      ],
      dest: paths.processed + '/img'
    },
    vendorJs: {
      src: [
        paths.lib + '/jquery/dist/jquery.min.js',
        paths.lib + '/box-sizing-polyfill/boxsizing.htc'
      ],
      dest: paths.processed + '/js/'
    }
  }
};
