var environment = require('./environment.js');

exports.config = {
  framework: 'jasmine2',
  specs: ['spec_suites/shared/*.js'],
  capabilities: {
    'browserName': 'chrome',
    'name': 'flapjack-browser-tests'
  },

  sauceUser: process.env.SAUCE_USER,
  sauceKey: process.env.SAUCE_KEY,

  onPrepare: function() {
    browser.ignoreSynchronization = true;

    var jasmineReporters = require('jasmine-reporters');
    var mkdirp = require('mkdirp');
    var jasmineSpecReporter = require('jasmine-spec-reporter');

    // add jasmine spec reporter
    jasmine.getEnv().addReporter(new jasmineSpecReporter({displayStacktrace: true}));

    // var folderName = (new Date()).toString().split(' ').splice(1, 4).join('-');
    var newFolder = "reports/";

    mkdirp(newFolder, function( err ) {
      if (err) {
        console.error(err);
      } else {
        var jUnitXmlReporter = new jasmineReporters.JUnitXmlReporter(
          {consolidateAll: true,
            savePath: newFolder,
            filePrefix: 'test-results'}
        );
        jasmine.getEnv().addReporter(jUnitXmlReporter);
      }
    });
  }
};
