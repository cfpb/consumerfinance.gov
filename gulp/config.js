'use strict';

const fs = require( 'fs' );
const paths = require( '../config/environment' ).paths;
const globAll = require( 'glob-all' );

module.exports = {
  pkg:    JSON.parse( fs.readFileSync( 'package.json' ) ), // eslint-disable-line no-sync, no-inline-comments, max-len
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
      ' *  <%= pkg.name %>\n' +
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
    tests: paths.test,
    reporter: process.env.CONTINUOUS_INTEGRATION // eslint-disable-line no-process-env
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
        paths.lib,
        paths.modules + '/cf-*/src',
        paths.modules + '/cfpb-chart-builder/src/**',
        paths.modules + '/highcharts/css'
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
      paths.legacy + '/nemo/_/js/AnalyticsTarget.js'
    ]
  },
  images: {
    src:  [ paths.unprocessed + '/img/**', './cfgov/wellbeing/static/img/**' ],
    dest: paths.processed + '/img'
  },
  copy: {
    codejson: {
      src:  'code.json',
      dest: paths.processed
    },
    icons: {
      src:  paths.modules + '/cf-icons/src/fonts/*',
      dest: paths.processed + '/fonts/'
    },
    vendorFonts: {
      src:  paths.unprocessed + '/fonts/pdfreactor/*',
      dest: paths.processed + '/fonts/pdfreactor'
    },
    vendorCss: {
      src: [
        paths.unprocessed + '/css/pdfreactor-fonts.css'
      ],
      dest: paths.processed + '/css'
    },
    vendorImg: {
      src: [],
      dest: paths.processed + '/img'
    },
    vendorJs: {
      src: [
        paths.modules + '/ustream-embedapi/dist/ustream-embedapi.min.js'
      ],
      dest: paths.processed + '/js/'
    }
  }
};
