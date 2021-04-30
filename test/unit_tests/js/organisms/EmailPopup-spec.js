import EmailPopup from '../../../../cfgov/unprocessed/js/organisms/EmailPopup.js';

let emailPopup;

const HTML_SNIPPET = `
<div class="o-email-popup o-email-signup" lang="en" data-popup-label="testPopup">
    <div class="o-email-popup_header u-clearfix">
        <div class="close">
            <button class="a-btn a-btn__link">Close</button>
        </div>
    </div>
    <div class="o-email-popup_body">
        <h2>Buying a home?</h2>
        <p>Sign up for email tips and info to help you through the process.</p>
        <form class="o-form o-form__email-signup u-clearfix"
              id="'o-email-signup_47"
              method="POST"
              action="#"
              enctype="application/x-www-form-urlencoded"
              novalidate>
              <div class="m-form-field">
                  <label class="u-visually-hidden" for="email_47">
                      Email address
                  </label>
                  <input class="a-text-input a-text-input__full"
                         id="email_47"
                         name="email"
                         type="email"
                         placeholder="Enter your email address"
                         required>
              </div>

              <div class="m-btn-group">
                  <button class="a-btn a-btn__full-on-xs">Sign up</button>
                  <a class="a-btn a-btn__link a-btn__secondary"
                     href="/owning-a-home/privacy-act-statement"
                     target="_blank"
                     rel="noopener noreferrer">
                      See Privacy Act statement
                  </a>
              </div>

              <input type="hidden" name="code" value="USCFPB_999">
        </form>
    </div>
    <div class="o-email-popup_footer">
        <div class="m-notification m-notification__success">
            <div class="m-notification_content">
                <div class="h4 m-notification_message">Success!</div>
            </div>
        </div>
    </div>
</div>
`;

describe( 'EmailPopup', () => {

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    emailPopup = new EmailPopup( document.querySelector( '.o-email-popup' ) );
    emailPopup.init();
  } );

  describe( 'init()', () => {
    it( 'should return the instance when initialized', () => {
      expect( emailPopup.init() ).toBeInstanceOf( EmailPopup );
    } );
  } );

  describe( 'getDom()', () => {
    it( 'should return the base element', () => {
      const baseElement = document.querySelector( '.o-email-popup' );
      expect( baseElement ).toStrictEqual( emailPopup.getDom() );
    } );
  } );

  describe( 'hidePopup()', () => {
    it( 'should remove CSS class that sets organism as hidden', () => {
      emailPopup.hidePopup();
      const baseElement = emailPopup.getDom();
      const containsClass = baseElement.classList.contains(
        'o-email-popup__visible'
      );
      expect( containsClass ).toBe( false );
    } );
  } );

  describe( 'showPopup()', () => {
    it( 'should not add CSS class that sets organism as visible ' +
        'if date is not set in local storage', () => {
      const isShown = emailPopup.showPopup();
      const baseElement = emailPopup.getDom();
      const containsClass = baseElement.classList.contains(
        'o-email-popup__visible'
      );
      expect( containsClass ).toBe( false );
      expect( isShown ).toBe( false );
    } );

    it( 'should add CSS class that sets organism as visible ' +
        'if date is set in local storage', () => {
      const days = 1;
      const date = new Date();
      const last = new Date( date.getTime() - ( days * 24 * 60 * 60 * 1000 ) );
      localStorage.setItem( 'testPopupPopupShowNext', last );
      const isShown = emailPopup.showPopup();
      const baseElement = emailPopup.getDom();
      const containsClass = baseElement.classList.contains(
        'o-email-popup__visible'
      );
      expect( containsClass ).toBe( true );
      expect( isShown ).toBe( true );
    } );
  } );
} );
