'use strict';

var fs = require( 'fs' );

/**
 * Set up file paths
 */
var loc = {
  src:  './src',
  dist: './dist',
  lib:  JSON.parse( fs.readFileSync( './.bowerrc' ) ).directory, // eslint-disable-line no-sync, no-inline-comments, max-len
  test: './test'
};

module.exports = {
  pkg:    JSON.parse( fs.readFileSync( 'bower.json' ) ), // eslint-disable-line no-sync, no-inline-comments, max-len
  banner:
      '/*!\n' +
      ' *               ad$$               $$\n' +
      ' *              d$"                 $$\n' +
      ' *              $$                  $$\n' +
      ' *   ,adPYba.   $$$$$  $$.,dPYba.   $$.,dPYba.\n' +
      ' *  aP′    `$:  $$     $$P′    `$a  $$P′    `$a\n' +
      ' *  $(          $$     $$(      )$  $$(      )$\n' +
      ' *  "b.    ,$:  $$     $$b.    ,$"  $$b.    ,$"\n' +
      ' *   `"Ybd$"′   $$     $$`"YbdP"′   $$`"YbdP"′\n' +
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
      loc.src + '/static/js/**/*.js',
      loc.test + '/unit_tests/**/*.js',
      loc.test + '/browser_tests/**/*.js'
    ],
    gulp: [
      'gulpfile.js',
      'gulp/**/*.js'
    ]
  },
  test: {
    src:   loc.src + '/static/js/**/*.js',
    tests: loc.test
  },
  clean: {
    dest: loc.dist
  },
  styles: {
    cwd:      loc.src + '/static/css',
    src:      '/main.less',
    dest:     loc.dist + '/static/css',
    settings: {
      paths: [
        loc.lib,
        loc.lib + '/cf-typography/src'
      ],
      compress: true
    }
  },
  scripts: {
    bundleConfigs: [
      {
        entries:    loc.src + '/static/js/routes/common.js',
        dest:       loc.dist + '/static/js/routes',
        outputName: 'common.min.js',
        require:    [
          'jquery',
          'jquery-easing',
          'cf-expandables',
          'chosen'
        ]
      }
    ]
  },
  images: {
    src:  loc.src + '/static/img/**',
    dest: loc.dist + '/static/img'
  },
  copy: {
    files: {
      src: [
        loc.src + '/**/*.html',
        loc.src + '/**/*.pdf',
        loc.src + '/_*/**/*',
        loc.src + '/robots.txt',
        '!' + loc.lib + '/**/*.html'
      ],
      dest: loc.dist
    },
    legacy: {
      src:  loc.src + '/static-legacy/**/*',
      dest: loc.dist + '/static-legacy'
    },
    icons: {
      src:  loc.lib + '/cf-icons/src/fonts/*',
      dest: loc.dist + '/static/fonts/'
    },
    vendorfonts: {
      src:  loc.src + '/static/fonts/pdfreactor/*',
      dest: loc.dist + '/static/fonts/pdfreactor'
    },
    vendorcss: {
      src: [
        loc.lib + '/slick-carousel/slick/slick.css',
        loc.lib + '/slick-carousel/slick/slick.css.map',
        loc.src + '/static/css/pdfreactor-fonts.css'
      ],
      dest: loc.dist + '/static/css'
    },
    vendorimg: {
      src: [
        loc.lib + '/slick-carousel/slick/ajax-loader.gif',
        loc.lib + '/chosen/chosen-sprite.png',
        loc.lib + '/chosen/chosen-sprite@2x.png'
      ],
      dest: loc.dist + '/static/img'
    },
    vendorjs: {
      src: [
        loc.lib + '/box-sizing-polyfill/boxsizing.htc',
        loc.lib + '/html5shiv/dist/html5shiv-printshiv.min.js'
      ],
      dest: loc.dist + '/static/js/'
    }
  }
};
