const fs = require( 'fs' );
const environment = require( '../config/environment' );
const paths = environment.paths;
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
    src: [
      `${ paths.unprocessed }/js/**/*.js`,
      `${ paths.unprocessed }/apps/**/js/**/*.js`,
      `!${ paths.unprocessed }/apps/**/node_modules/**`
    ],
    test:  [
      paths.test + '/util/**/*.js',
      paths.test + '/unit_tests/**/*.js',
      paths.test + '/browser_tests/**/*.js'
    ],
    build: [
      'config/**/*.js',
      'gulpfile.js',
      'gulp/**/*.js',
      'scripts/npm/**/*.js',
      'jest.config.js'
    ]
  },
  test: {
    src: [
      paths.unprocessed + '/apps/**/js/**/*.js',
      paths.unprocessed + '/js/**/*.js'
    ],
    reporter: environment.CONTINUOUS_INTEGRATION
  },
  clean: {
    css: paths.processed + '/css',
    js: paths.processed + '/js',
    dest: paths.processed
  },
  scripts: {
    src: paths.unprocessed + '/js/**/*.js',
    otherBuildTriggerFiles: [
      paths.unprocessed + '/js/**/*.js',
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
        paths.modules + '/cf-*/src',
        paths.modules + '/cfpb-chart-builder/src/**',
        paths.modules + '/highcharts/css'
      ] ),
      compress: true
    },
    otherBuildTriggerFiles: [
      paths.unprocessed + '/css/**/*.less',
      paths.modules,
      './config/**/*.js',
      './gulp/**/*.js'
    ],
    otherBuildTriggerFilesKBSpanish: [
      paths.legacy + '/knowledgebase/**/*.css',
      paths.legacy + '/knowledgebase/**/*.less'
    ],
    otherBuildTriggerFilesNemo: [
      paths.legacy + '/nemo/**/*.css',
      paths.legacy + '/nemo/**/*.less'
    ]
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
  copy: {
    jsonCode: {
      src:  'code.json',
      dest: paths.processed
    },
    jsonKBYO: {
      src:  `${ paths.unprocessed }/apps/know-before-you-owe/js/kbyo-timeline.json`,
      dest: `${ paths.processed }/apps/know-before-you-owe/js`
    },
    icons: {
      src:  paths.modules + '/cf-icons/src/fonts/*',
      dest: paths.processed + '/fonts/'
    },
    timelinejs: {
      src: [
        paths.modules + '/timelinejs/build/**/*'
      ],
      dest: paths.processed + '/apps/timelinejs'
    },
    lightbox2: {
      src: [
        paths.modules + '/lightbox2/dist/**/*'
      ],
      dest: paths.processed + '/lightbox2'
    },
    vendorJs: {
      src: [
        paths.modules + '/ustream-embedapi/dist/ustream-embedapi.min.js'
      ],
      dest: paths.processed + '/js/'
    }
  }
};
