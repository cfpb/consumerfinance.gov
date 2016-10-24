/* ==========================================================================
   Scripts for Email Signup organism.
   ========================================================================== */

'use strict';

var EmailSignup = require( '../../organisms/EmailSignup.js' );
var emailSignup = new EmailSignup( document.body.querySelector( EmailSignup.selector ));

emailSignup.init();
