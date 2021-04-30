import FormSubmit from '../../../../cfgov/unprocessed/js/organisms/FormSubmit.js';

const BASE_CLASS = 'o-email-signup';
const HTML_SNIPPET = `
<div class="o-email-signup">
    <header class="m-slug-header">
        <h2 class="a-heading">
            Stay informed
        </h2>
    </header>
    <p>
        Subscribe to our email newsletter. We will update you on new blogs.
    </p>
    <form class="o-form o-form__email-signup"
          id="o-form__email-signup_371b6fce64d1b6"
          method="POST"
          action="/subscriptions/new/"
          enctype="application/x-www-form-urlencoded">
        <div class="u-mb15">
            <div class="m-notification">
                <div class="m-notification_content">
                    <div class="h4 m-notification_message"></div>
                </div>
            </div>
        </div>
        <div class="m-form-field">
            <label class="a-label a-label__heading" for="email_371b6fce64d1b6">
                Email address
            </label>
            <input class="a-text-input a-text-input__full"
                   id="email_371b6fce64d1b6"
                   name="email"
                   type="email"
                   placeholder="mail@example.com"
                   required="">
        </div>
        <div class="m-btn-group">
            <button class="a-btn">Sign up</button>
            <a class="a-btn a-btn__link a-btn__secondary"
               href="/owning-a-home/privacy-act-statement/"
               target="_blank"
               rel="noopener noreferrer">
                See Privacy Act statement
            </a>
        </div>
        <input type="hidden" name="code" value="USCFPB_127">
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
      expect( formSubmit.init() ).toBeInstanceOf( FormSubmit );
    } );
  } );
} );
