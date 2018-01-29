/* ==========================================================================
   Common application-wide scripts for owning-a-home.
   ========================================================================== */

const Notification = require( '../../../js/molecules/Notification' );
const FormSubmit = require( '../../../js/organisms/FormSubmit.js' );
const validators = require( '../../../js/modules/util/validators' );
const ratingsForm = require( './ratings-form' );

const BASE_CLASS = 'o-email-signup';
const emailSignup = document.body.querySelector( '.' + BASE_CLASS );

if ( emailSignup ) {
  const _notification = new Notification( 'emailSignup' );
  _notification.init();

  const language = document.body.querySelector( '.content' ).lang;
  const formSubmit = new FormSubmit(
    emailSignup,
    _notification,
    BASE_CLASS,
    {
      validator: fields => validators.email(
        fields.email, '', { language: language }
      ).msg,
      language: language
    }
  );

  formSubmit.init();
}

ratingsForm.init();
