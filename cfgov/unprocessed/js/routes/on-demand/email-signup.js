/* ==========================================================================
   Scripts for Email Signup organism.
   ========================================================================== */

'use strict';

var EmailSignup = require( '../../organisms/EmailSignup.js' );
var emailSignup = new EmailSignup(
  document.body.querySelector( EmailSignup.BASE_CLASS )
);

emailSignup.init();
