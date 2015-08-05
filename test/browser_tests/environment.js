'use strict';

// Common configuration files with defaults plus overrides from environment vars
var webServerDefaultPort = 7000;

module.exports = {
  // The address of a running selenium server.
  seleniumAddress:
    process.env.SELENIUM_URL || 'http://localhost:4444/wd/hub',

  // Default http port to host the web server
  webServerDefaultPort: webServerDefaultPort,

  // Protractor interactive tests
  interactiveTestPort: 6969,

  // A base URL for your application under test.
  baseUrl:
    'http://' + ( process.env.HTTP_HOST || 'localhost' ) +
          ':' + ( process.env.HTTP_PORT || webServerDefaultPort )

};
