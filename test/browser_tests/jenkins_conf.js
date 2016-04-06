'use strict';

var JasmineReporters = require( 'jasmine-reporters' );
var JasmineSpecReporter = require( 'jasmine-spec-reporter' );
var mkdirp = require( 'mkdirp' );
var environment = require( './environment.js' );

exports.config = {
  framework:    'jasmine2',
  specs:        [ environment.specsBasePath + '.js' ],
  capabilities: {
    'browserName':       'chrome',
    'name':              'flapjack-browser-tests ' + process.env.SITE_DESC,
    'tunnel-identifier': process.env.SAUCE_TUNNEL
  },

  sauceUser: process.env.SAUCE_USER,
  sauceKey:  process.env.SAUCE_KEY,

  onPrepare: function() {
    browser.ignoreSynchronization = true;

    // Add jasmine spec reporter.
    jasmine.getEnv().addReporter(
      new JasmineSpecReporter( { displayStacktrace: true } )
    );

    var newFolder = 'reports/';

    mkdirp( newFolder, function( err ) {
      if ( err ) {
        console.error( err ); // eslint-disable-line no-console, no-inline-comments, max-len
      } else {
        var jUnitXmlReporter = new JasmineReporters.JUnitXmlReporter( {
          consolidateAll: true,
          savePath:       newFolder,
          filePrefix:     'test-results'
        } );
        jasmine.getEnv().addReporter( jUnitXmlReporter );
      }
    } );
  }
};
