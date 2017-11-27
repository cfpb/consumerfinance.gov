/* ==========================================================================
   Common application-wide scripts for owning-a-home.
   ========================================================================== */

var FormSubmit = require( '../../organisms/FormSubmit.js' );
var validators = require( '../../modules/util/validators' );
var ratingsForm = require( '../../apps/owning-a-home/ratings-form' );
var BASE_CLASS = 'o-email-signup';
var emailSignup = document.body.querySelector( '.' + BASE_CLASS );

if ( emailSignup ) {
  var language = document.body.querySelector( '.content' ).lang;
  var formSubmit = new FormSubmit( emailSignup, BASE_CLASS,
    { validator: fields => {
        return validators.email( fields.email, '', { language: language } )
               .msg;
      },
      language: language
    }
  );

  formSubmit.init();
}

ratingsForm.init();
