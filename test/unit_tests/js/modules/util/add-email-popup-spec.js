const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/modules/util';

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

describe( 'add-email-popup', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
  } );

  it( 'should hide the email popup initially', () => {
    // eslint-disable-next-line no-unused-vars
    const addEmailPopup = require( BASE_JS_PATH + '/add-email-popup' );
    const emailPopupDom = document.querySelector( '.o-email-popup' );
    expect( emailPopupDom.classList.contains( 'o-email-popup__visible' ) )
      .toBe( false );
  } );
} );
