const environmentTest = require( './environmentTest' );
const envvars = require( '../../config/environment' ).envvars;
const JasmineReporters = require( 'jasmine-reporters' );
const JasmineSpecReporter = require( 'jasmine-spec-reporter' );
const mkdirp = require( 'mkdirp' );

exports.config = {
  framework:    'jasmine2',
  specs:        [ environmentTest.specsBasePath + '.js' ],
  capabilities: {
    'browserName':       'chrome',
    'name':              'flapjack-browser-tests ' + envvars.SITE_DESC,
    'tunnel-identifier': envvars.SAUCE_TUNNEL
  },

  sauceUser: envvars.SAUCE_USERNAME,
  sauceKey:  envvars.SAUCE_ACCESS_KEY,

  onPrepare: function() {
    // Ignore Selenium allowances for non-angular sites.
    browser.ignoreSynchronization = true;

    // Add jasmine spec reporter.
    jasmine.getEnv().addReporter(
      new JasmineSpecReporter( { displayStacktrace: true } )
    );

    const newFolder = 'reports/';

    mkdirp( newFolder, function( err ) {
      if ( err ) {
        console.error( err );
      } else {
        const jUnitXmlReporter = new JasmineReporters.JUnitXmlReporter( {
          consolidateAll: true,
          savePath:       newFolder,
          filePrefix:     'test-results'
        } );
        jasmine.getEnv().addReporter( jUnitXmlReporter );
      }
    } );
  }
};
