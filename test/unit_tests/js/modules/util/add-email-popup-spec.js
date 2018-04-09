const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/modules/util';
const storageMock = require( '../../../../util/mock-web-storage' );
const iconsPath = '../../../../node_modules/cf-icons/src/icons/';
const closeIcon = require( iconsPath + 'close.svg' );
const informationRoundIcon = require( iconsPath + 'information-round.svg' );
let addEmailPopup;

const HTML_SNIPPET = `
<div class="o-email-popup o-email-popup__visible" lang="en" data-popup-label="testPopup">
    <div class="o-email-popup_header">
        <div class="close">
            <a>Close ${closeIcon}</a>
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
                            m-notification__success
                            ">
                    ${informationRoundIcon}
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

describe( 'add-email-popup', () => {
  beforeAll( () => {
    // Mock the window's web storage APIs.
    window.localStorage = storageMock( {} );
    window.sessionStorage = storageMock( {} );
  } );

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
  } );

  it( 'should hide the email popup initially', () => {
    addEmailPopup = require( BASE_JS_PATH + '/add-email-popup' );
    const emailPopupDom = document.querySelector( '.o-email-popup' );
    expect( emailPopupDom.classList.contains( 'o-email-popup__visible' ) )
      .toBe( false );
  } );
} );
