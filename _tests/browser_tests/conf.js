var env = require('./environment.js');

exports.config = {
  specs: ['spec_suites/shared/*.js'],
  multiCapabilities: [
    {
      'browserName': 'chrome',
    },
    {
      'browserName': 'firefox',
    },
    // Large Screen only tests
    {
      'browserName': 'chrome',
      'chromeOptions' : {
        args: ['--lang=en',
               '--window-size=1200,900']
      },
      specs: ['spec_suites/large_screen/*.js']
    }
  ],

  baseUrl: env.baseUrl,

  onPrepare: function() {
    return browser.ignoreSynchronization = true;
  }
};
