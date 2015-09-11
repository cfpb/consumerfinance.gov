'use strict';

var fs = require( 'fs' );

/**
 * Set up file paths
 */
var loc = {
  v1:  './cfgov/v1/preprocessed',
  templates: './cfgov/v1/jinja2/v1',
  dist: './cfgov/v1/static',
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
      loc.v1 + '/js/**/*.js',
      loc.test + '/unit_tests/**/*.js',
      loc.test + '/browser_tests/**/*.js'
    ],
    gulp: [
      'gulpfile.js',
      'gulp/**/*.js'
    ]
  },
  test: {
    src:   loc.v1 + '/js/**/*.js',
    tests: loc.test
  },
  clean: {
    dest: loc.dist
  },
  styles: {
    cwd:      loc.v1 + '/css',
    src:      '/main.less',
    dest:     loc.dist + '/css',
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
        entries:    loc.v1 + '/js/routes/common.js',
        dest:       loc.dist + '/js/routes',
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
    src:  loc.v1 + '/img/**',
    dest: loc.dist + '/img'
  },
  copy: {
    files: {
      src: '!' + loc.lib + '/**/*.html',
      dest: loc.templates
    },
    icons: {
      src:  loc.lib + '/cf-icons/src/fonts/*',
      dest: loc.dist + '/fonts/'
    },
    vendorfonts: {
      src:  loc.v1 + '/fonts/pdfreactor/*',
      dest: loc.dist + '/fonts/pdfreactor'
    },
    vendorcss: {
      src: [
        loc.lib + '/slick-carousel/slick/slick.css',
        loc.lib + '/slick-carousel/slick/slick.css.map',
        loc.v1 + '/css/pdfreactor-fonts.css'
      ],
      dest: loc.dist + '/css'
    },
    vendorimg: {
      src: [
        loc.lib + '/slick-carousel/slick/ajax-loader.gif',
        loc.lib + '/chosen/chosen-sprite.png',
        loc.lib + '/chosen/chosen-sprite@2x.png'
      ],
      dest: loc.dist + '/img'
    },
    vendorjs: {
      src: [
        loc.lib + '/box-sizing-polyfill/boxsizing.htc',
        loc.lib + '/html5shiv/dist/html5shiv-printshiv.min.js'
      ],
      dest: loc.dist + '/js/'
    }
  }
};
