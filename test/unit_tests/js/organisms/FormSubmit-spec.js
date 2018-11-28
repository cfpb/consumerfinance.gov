import FormSubmit from '../../../../cfgov/unprocessed/js/organisms/FormSubmit';

const BASE_CLASS = 'o-email-signup';
const HTML_SNIPPET = `
<div class="o-email-signup">
  <header class="m-slug-header">
    <h2 class="a-heading">
      Stay informed
    </h2>
  </header>

  <form id="o-email-signup_54"
        class="o-form o-form__email-signup"
        action="/subscriptions/new/"
        method="POST"
        enctype="application/x-www-form-urlencoded">

    <div class="u-mb15">
      <div class="m-notification
                  m-notification__success">
        <div class="m-notification_content">
          <div class="h4 m-notification_message"></div>
        </div>
      </div>
    </div>

    <p>Subscribe to our email newsletter. We will update you on new blogs.</p>

    <div class="m-form-field-with-button" data-qa-hook="formfield-with-button">
      <div class="m-form-field">
        <label class="a-label a-label__heading" for="form_3">
          Email address
        </label>
        <input id="form_3"
               type="email"
               placeholder="example@mail.com"
               name="email"
               class="a-text-input a-text-input__full">
      </div>
      <p>
        The information you provide will permit the Consumer Financial
        Protection Bureau to process your request or
        inquiry.&nbsp;<a class="" href="/privacy/privacy-policy/">See more</a>.
      </p>
      <input class="a-btn a-btn__full-on-xs" type="submit" value="Sign up">
    </div>

    <div class="form-group">
      <input type="hidden" name="code">
    </div>

  </form>
</div>
`;

describe( 'FormSubmit', () => {
  let signupForm;
  let formSubmit;
  let thisFormSubmit;

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    signupForm = document.querySelector( `.${ BASE_CLASS }` );
    formSubmit = new FormSubmit( signupForm, BASE_CLASS, {} );
    thisFormSubmit = formSubmit.init();
  } );

  describe( 'init()', () => {
    it( 'should return the FormSubmit instance when initialized', () => {
      expect( typeof thisFormSubmit ).toStrictEqual( 'object' );
      expect( signupForm.dataset.jsHook ).toStrictEqual( 'state_atomic_init' );
    } );

    it( 'should return undefined if already initialized', () => {
      expect( formSubmit.init() ).toBeUndefined();
    } );
  } );
} );
