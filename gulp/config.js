'use strict';

var fs = require( 'fs' );
var paths = require( '../config/environment' ).paths;

module.exports = {
  pkg:    JSON.parse( fs.readFileSync( 'bower.json' ) ), // eslint-disable-line no-sync, no-inline-comments, max-len
  banner:
      '/*!\n' +
      ' *               ad$$               $$\n' +
      ' *              d$"                 $$\n' +
      ' *              $$                  $$\n' +
      ' *   ,adPYba.   $$$$$  $$.,dPYba.   $$.,dPYba.\n' +
      ' *  aP‘    `$:  $$     $$P‘    `$a  $$P‘    `$a\n' +
      ' *  $(          $$     $$(      )$  $$(      )$\n' +
      ' *  "b.    ,$:  $$     $$b.    ,$"  $$b.    ,$"\n' +
      ' *   `"Ybd$"‘   $$     $$`"YbdP"‘   $$`"YbdP"‘\n' +
      ' *                     $$\n' +
      ' *                     $$\n' +
      ' *                     $$\n' +
      ' *\n' +
      ' *  <%= pkg.name %> - v<%= pkg.version %>\n' +
      ' *  <%= pkg.homepage %>\n' +
      ' *  A public domain work of the Consumer Financial Protection Bureau\n' +
      ' */\n',
  lint: {
    src: [
      paths.src + '/static/js/**/*.js',
      paths.test + '/unit_tests/**/*.js',
      paths.test + '/browser_tests/**/*.js'
    ],
    gulp: [
      'gulpfile.js',
      'gulp/**/*.js'
    ]
  },
  test: {
    src:   paths.src + '/static/js/**/*.js',
    tests: paths.test
  },
  clean: {
    dest: paths.dist
  },
  styles: {
    cwd:      paths.src + '/static/css',
    src:      '/main.less',
    dest:     paths.dist + '/static/css',
    settings: {
      paths: [
        paths.lib,
        paths.lib + '/cf-typography/src'
      ],
      compress: true
    }
  },
  images: {
    src:  paths.src + '/static/img/**',
    dest: paths.dist + '/static/img'
  },
  copy: {
    files: {
      src: [
        paths.src + '/**/*.html',
        paths.src + '/**/*.pdf',
        paths.src + '/_*/**/*',
        paths.src + '/robots.txt',
        paths.src + '/favicon.ico',
        '!' + paths.lib + '/**/*.html'
      ],
      dest: paths.dist
    },
    legacy: {
      src:  paths.src + '/static-legacy/**/*',
      dest: paths.dist + '/static-legacy'
    },
    icons: {
      src:  paths.lib + '/cf-icons/src/fonts/*',
      dest: paths.dist + '/static/fonts/'
    },
    vendorfonts: {
      src:  paths.src + '/static/fonts/pdfreactor/*',
      dest: paths.dist + '/static/fonts/pdfreactor'
    },
    vendorcss: {
      src: [
        paths.lib + '/slick-carousel/slick/slick.css',
        paths.lib + '/slick-carousel/slick/slick.css.map',
        paths.src + '/static/css/pdfreactor-fonts.css'
      ],
      dest: paths.dist + '/static/css'
    },
    vendorimg: {
      src: [
        paths.lib + '/slick-carousel/slick/ajax-loader.gif',
        paths.lib + '/chosen/chosen-sprite.png',
        paths.lib + '/chosen/chosen-sprite@2x.png'
      ],
      dest: paths.dist + '/static/img'
    },
    vendorjs: {
      src: [
        paths.lib + '/jquery/dist/jquery.min.js',
        paths.lib + '/box-sizing-polyfill/boxsizing.htc',
        paths.lib + '/html5shiv/dist/html5shiv-printshiv.min.js'
      ],
      dest: paths.dist + '/static/js/'
    }
  }
};
