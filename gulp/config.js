const fs = require( 'fs' );
const environment = require( '../config/environment' );
const paths = environment.paths;
const globAll = require( 'glob-all' );

module.exports = {
  // eslint-disable-next-line no-sync
  pkg:    JSON.parse( fs.readFileSync( 'package.json' ) ),
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
    src: [
      `${ paths.unprocessed }/js/**/*.js`,
      `${ paths.unprocessed }/apps/**/js/**/*.js`,
      `!${ paths.unprocessed }/apps/**/node_modules/**`
    ],
    test: [
      paths.test + '/cypress/**/*.js',
      paths.test + '/util/**/*.js',
      paths.test + '/unit_tests/**/*.js'
    ],
    build: [
      'config/**/*.js',
      'gulpfile.js',
      'gulp/**/*.js',
      'scripts/npm/**/*.js',
      'jest.config.js'
    ]
  },
  scripts: {
    src: paths.unprocessed + '/js/**/*.js',
    otherBuildTriggerFiles: [
      paths.unprocessed + '/js/**/*.js',
      paths.unprocessed + '/apps/**/js/**/*.js',
      paths.modules,
      './config/**/*.js',
      './gulp/**/*.js'
    ]
  },
  styles: {
    cwd:      paths.unprocessed + '/css',
    src:      '/main.less',
    dest:     paths.processed + '/css',
    settings: {
      paths:  globAll.sync( [
        paths.modules + '/@cfpb/cfpb-*/src',
        paths.modules + '/cfpb-chart-builder/src/**',
        paths.modules + '/highcharts/css'
      ] ),
      compress: true
    },
    otherBuildTriggerFiles: [
      paths.unprocessed + '/css/**/*.css',
      paths.unprocessed + '/css/**/*.less',
      paths.unprocessed + '/apps/**/css/**/*.less',
      paths.modules,
      './config/**/*.js',
      './gulp/**/*.js'
    ]
  }
};
