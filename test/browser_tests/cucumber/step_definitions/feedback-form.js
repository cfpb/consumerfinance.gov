const { Then, When, Before } = require( 'cucumber' );
const chai = require( 'chai' );
const expect = chai.expect;
const chaiAsPromised = require( 'chai-as-promised' );

const BASE_SEL = '.o-feedback';
const FORM = BASE_SEL + ' .o-form';
const COMMENT_FIELD = BASE_SEL + ' #comment';
const RADIO_BUTTON_1 = BASE_SEL + ' #is_helpful_1';
const SUBMIT_BUTTON = BASE_SEL + ' [type="submit"]';
const NOTIFICATION = BASE_SEL + ' .m-notification';
const SUCCESS_CLASS = 'm-notification__success';
const ERROR_CLASS = 'm-notification__error';

chai.use( chaiAsPromised );

let _dom;

Before( function() {
  _dom = {
    radioButton1: element( by.css( RADIO_BUTTON_1 ) ),
    commentField: element( by.css( COMMENT_FIELD ) ),
    submitButton: element( by.css( SUBMIT_BUTTON ) ),
    form:         element( by.css( FORM ) ),
    notification: element( by.css( NOTIFICATION ) )
  };
} );

When( 'I select a feedback radio button',
  function() {
    return browser.executeScript(
      'arguments[0].click();',
      _dom.radioButton1.getWebElement()
    );
  }
);

When( 'I enter a comment',
  function() {
    return _dom.commentField.sendKeys( 'comment text' );
  }
);

When( 'I click the feedback form submit button',
  async function() {
    _dom.submitButton.click();
    return await browser.sleep( 500 );
  }
);

Then( 'the notification element should be displayed',
  function( ) {
    return expect( _dom.notification.isDisplayed() )
      .to.eventually.equal( true );
  }
);

Then( 'the notification should report an error',
  function( ) {
    const notificationClasses =
      _dom.notification.getAttribute( 'class' );
    return expect( notificationClasses )
      .to.eventually
      .contain( ERROR_CLASS );
  }
);

Then( 'the notification should report success',
  function( ) {
    const notificationClasses =
      _dom.notification.getAttribute( 'class' );
    return expect( notificationClasses )
      .to.eventually
      .contain( SUCCESS_CLASS );
  }
);

Then( 'the feedback form should be present',
  function( ) {
    return expect( _dom.form.isPresent() )
      .to.eventually.equal( true );
  }
);

Then( 'the feedback form should no longer be present',
  function( ) {
    return expect( _dom.form.isPresent() )
      .to.eventually.equal( false );
  }
);
