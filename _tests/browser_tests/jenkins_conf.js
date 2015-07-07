var env = require('./environment.js');

exports.config = {
  specs: ['spec_suites/shared/*.js'],
  capabilities: {
    'browserName': 'chrome',
    'name': 'flapjack-browser-tests'
  },
  sauceUser: process.env.SAUCE_USER,
  sauceKey: process.env.SAUCE_KEY,

  onPrepare: function() {
    return browser.ignoreSynchronization = true;
  }
};