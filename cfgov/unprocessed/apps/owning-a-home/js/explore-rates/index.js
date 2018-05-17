// Auto-polyfill Promise for IE11.
require( 'es6-promise' ).polyfill();

import * as rateChecker from './rate-checker';

// Do it!
rateChecker.init();
