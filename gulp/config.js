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
      paths.preproccesed + '/js/**/*.js',
      paths.test + '/unit_tests/**/*.js',
      paths.test + '/browser_tests/**/*.js'
    ],
    gulp: [
      'gulpfile.js',
      'gulp/**/*.js'
    ]
  },
  test: {
    src:   paths.preproccesed + '/js/**/*.js',
    tests: paths.test
  },
  clean: {
    dest: paths.processed
  },
  styles: {
    cwd:      paths.preproccesed + '/css',
    src:      '/main.less',
    dest:     paths.processed + '/css',
    settings: {
      paths: [
        paths.lib,
        paths.lib + '/cf-typography/src'
      ],
      compress: true
    }
  },
  images: {
    src:  paths.preproccesed + '/img/**',
    dest: paths.processed + '/img'
  },
  copy: {
    icons: {
      src:  paths.lib + '/cf-icons/src/fonts/*',
      dest: paths.processed + '/fonts/'
    },
    vendorfonts: {
      src:  paths.preproccesed + '/fonts/pdfreactor/*',
      dest: paths.processed + '/fonts/pdfreactor'
    },
    vendorcss: {
      src: [
        paths.lib + '/slick-carousel/slick/slick.css',
        paths.lib + '/slick-carousel/slick/slick.css.map',
        paths.preproccesed + '/css/pdfreactor-fonts.css'
      ],
      dest: paths.processed + '/css'
    },
    vendorimg: {
      src: [
        paths.lib + '/slick-carousel/slick/ajax-loader.gif',
        paths.lib + '/chosen/chosen-sprite.png',
        paths.lib + '/chosen/chosen-sprite@2x.png'
      ],
      dest: paths.processed + '/img'
    },
    vendorjs: {
      src: [
        paths.lib + '/jquery/dist/jquery.min.js',
        paths.lib + '/box-sizing-polyfill/boxsizing.htc',
        paths.lib + '/html5shiv/dist/html5shiv-printshiv.min.js'
      ],
      dest: paths.processed + '/js/'
    }
  }
};
