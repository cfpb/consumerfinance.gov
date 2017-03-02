'use strict';

var environment = require( './environment.js' );
var JasmineReporters = require( 'jasmine-reporters' );
var JasmineSpecReporter = require( 'jasmine-spec-reporter' );
var mkdirp = require( 'mkdirp' );

exports.config = {
  framework:    'jasmine',

  seleniumServerJar: '../../node_modules/protractor/node_modules/webdriver-manager/selenium/selenium-server-standalone-3.2.0.jar',
  //seleniumServerJar: '/Users/muchniki/.nvm/versions/node/v6.9.5/lib/node_modules/protractor/node_modules/webdriver-manager/selenium/selenium-server-standalone-3.1.0.jar',
  //port of the server
  seleniumPort: 4444,
  seleniumArgs: ['-browserTimeout=60'],
  //seleniumAddress: 'http://localhost:4444/wd/hub',
  troubleshoot: false, //true if you want to see actual web-driver configuration
  capabilities: {
    'browserName': 'phantomjs',
    //Can be used to specify the phantomjs binary path.
    //This can generally be ommitted if you installed phantomjs globally.
    'phantomjs.binary.path': require('phantomjs').path,
    'phantomjs.cli.args': ['--ignore-ssl-errors=true', '--web-security=false']
  },

  specs: [ environment.specsBasePath + '.js' ],
  allScriptsTimeout: 60000,
  getPageTimeout: 60000,
  onPrepare: function() {
    // Ignore Selenium allowances for non-angular sites.
    browser.ignoreSynchronization = true;

    // Add jasmine spec reporter.
    // jasmine.getEnv().addReporter(
    //   new JasmineSpecReporter( { displayStacktrace: true } )
    // );true

    // jasmine.getEnv().addReporter(
    //   new jasmine.JUnitXmlReporter('protractor-results', true, true)
    // );

    var newFolder = 'reports/';

    mkdirp( newFolder, function( err ) {
      if ( err ) {
        console.error( err );
      } else {
        var jUnitXmlReporter = new JasmineReporters.JUnitXmlReporter( {
          consolidateAll: true,
          savePath:       newFolder,
          filePrefix:     'test-results'
        } );
        jasmine.getEnv().addReporter( jUnitXmlReporter );
      }
    } );
  },

  jasmineNodeOpts: {
    showColors: true,
    defaultTimeoutInterval: 60000,
    isVerbose: false,
    includeStackTrace: false
  }

};
