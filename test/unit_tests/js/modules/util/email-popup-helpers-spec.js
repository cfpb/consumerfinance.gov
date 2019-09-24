const BASE_JS_PATH = '../../../../../unprocessed/js/';
const emailPopupsHelpers = require(
  BASE_JS_PATH + 'modules/util/email-popup-helpers'
);
describe( 'email-popup-helpers', () => {
  describe( 'showEmailPopup()', () => {
    it( 'should return true if no date is in storage', () => {
      expect( emailPopupsHelpers.showEmailPopup( 'testPopup' ) ).toBe( true );
    } );

    it( 'should return true if date in storage is before today', () => {
      // Days you want to subtract.
      const days = 1;
      const date = new Date();
      const last = new Date( date.getTime() - ( days * 24 * 60 * 60 * 1000 ) );
      localStorage.setItem( 'testPopupPopupShowNext', last );
      expect( emailPopupsHelpers.showEmailPopup( 'testPopup' ) ).toBe( true );
    } );
  } );

  describe( 'recordEmailPopupView()', () => {
    it( 'should record number of times popup has been shown', () => {
      emailPopupsHelpers.recordEmailPopupView( 'testPopup' );
      expect( localStorage.getItem( 'testPopupPopupCount' ) ).toBe( '1' );
      emailPopupsHelpers.recordEmailPopupView( 'testPopup' );
      expect( localStorage.getItem( 'testPopupPopupCount' ) ).toBe( '2' );
    } );
  } );

  describe( 'recordEmailRegistration()', () => {
    it( 'should set email popup key in local storage with ' +
        'a very long expiry date', () => {
      emailPopupsHelpers.recordEmailRegistration( 'testPopup' );
      const date = new Date();
      const testDate = date.setTime(
        date.getTime() + ( 10000 * 24 * 60 * 60 * 1000 )
      );

      /* To avoid being off by a millisecond, we need to convert to a decimal
         and check using toBeCloseTo matcher instead of toBe. */
      expect( localStorage.getItem( 'testPopupPopupShowNext' ) / 10000 )
        .toBeCloseTo( testDate / 10000 );
    } );
  } );

  describe( 'recordEmailPopupClosure()', () => {
    it( 'should record in local storage that ' +
        'the email popup has been closed.', () => {
      emailPopupsHelpers.recordEmailPopupClosure( 'testPopup' );
      const date = new Date();
      const testDate = date.setTime(
        date.getTime() + ( 60 * 24 * 60 * 60 * 1000 )
      );
      expect( localStorage.getItem( 'testPopupPopupCount' ) ).toBe( '2' );

      /* To avoid being off by a millisecond, we need to convert to a decimal
         and check using toBeCloseTo matcher instead of toBe. */
      const valueStore = localStorage.getItem( 'testPopupPopupShowNext' );
      expect( Number.parseInt( valueStore, 10 ) / 10000 )
        .toBeCloseTo( testDate / 10000 );
    } );
  } );
} );
