const config = require( './conf' ).config;

config.plugins = [ {
  'axe':     true,
  'package': 'protractor-accessibility-plugin'
} ];

exports.config = config;
