/* ==========================================================================
   Common application-wide scripts for owning-a-home.
   ========================================================================== */

import * as ratingsForm from './ratings-form';
import * as validators from '../../../js/modules/util/validators';
import FormSubmit from '../../../js/organisms/FormSubmit.js';

const BASE_CLASS = 'o-email-signup';
const emailSignup = document.body.querySelector( '.' + BASE_CLASS );

if ( emailSignup ) {
  const language = document.body.querySelector( '.content' ).lang;
  const formSubmit = new FormSubmit(
    emailSignup,
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
