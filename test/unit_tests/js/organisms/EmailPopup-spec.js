import EmailPopup from '../../../../cfgov/unprocessed/js/organisms/EmailPopup';

let emailPopup;

const HTML_SNIPPET = `
<div class="o-email-popup" lang="en" data-popup-label="testPopup">
    <div class="o-email-popup_header">
        <div class="close">
            <a>Close</a>
        </div>
    </div>
    <div class="o-email-popup_body">
        <div class="o-email-signup">
            <h2>Buying a home?</h2>
            <form class="o-form o-form__email-signup">
                <p>Sign up for email tips and info to help you through the process.</p>
                <div class="m-form-field-with-button">
                    <div class="form-group">
                        <input id="form_18" type="email" placeholder="Enter your email address" name="email" class="m-form-field-with-button_field a-text-input" required="">
                    </div>
                    <p>
                        <a href="/owning-a-home-privacy-act-statement/" target="_blank" rel="noopener noreferrer">Privacy Act statement</a>
                        <br>
                    </p>
                    <input class="a-btn a-btn__full-on-xs" type="submit" value="Sign up">
                </div>
                <div class="form-group">
                    <input type="hidden" name="code" value="USCFPB_128">
                </div>
            </form>
            <div class="o-email-signup_footer">
                <div class="m-notification
                            m-notification__success">
                    <div class="m-notification_content">
                        <div class="h4 m-notification_message"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="o-email-popup_footer"></div>
</div>
`;

describe( 'EmailPopup', () => {

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    emailPopup = new EmailPopup( document.querySelector( '.o-email-popup' ) );
    emailPopup.init();
  } );

  describe( 'init()', () => {
    it( 'should return undefined if already initialized', () => {
      expect( emailPopup.init() ).toBeUndefined();
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
