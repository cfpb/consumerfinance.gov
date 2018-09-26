const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const utils = require( `${ BASE_JS_PATH }/js/permalinks-utils.js` );

const HTML_SNIPPET1 = `
  <div class="regdown-block" id="Interp-1"></div>
  <div class="regdown-block" id="c"></div>
  <div class="regdown-block" id="z-14-i"></div>
`;

const HTML_SNIPPET2 = `
  <div class="regdown-block" id="a"></div>
  <div class="regdown-block" id="b"></div>
  <div class="regdown-block" id="c"></div>
  <div class="regdown-block" id="d"></div>
  <div class="regdown-block" id="e"></div>
`;

describe( 'The Regs3K permalinks utils', () => {

  describe( 'Debounce', () => {

    beforeEach( () => {
      global.spy = done => {
        if ( done ) done();
      };
    } );

    it( 'should only call a function once within a given timespan', done => {
      const event = document.createEvent( 'Event' );
      event.initEvent( 'resize', true, true );
      jest.spyOn( global, 'spy' );

      utils.debounce( 'resize', 100, global.spy );

      // Fire the event three times
      window.dispatchEvent( event );
      window.dispatchEvent( event );
      window.dispatchEvent( event );

      // It should have only been called once
      setTimeout( () => {
        expect( global.spy ).toHaveBeenCalledTimes( 1 );
        done();
      }, 200 );
    } );

    it( 'should not call a function if the timespan hasn\'t passed', done => {
      const event = document.createEvent( 'Event' );
      event.initEvent( 'scroll', true, true );
      jest.spyOn( global, 'spy' );

      utils.debounce( 'scroll', 1000, global.spy );

      // Fire the event three times
      window.dispatchEvent( event );
      window.dispatchEvent( event );
      window.dispatchEvent( event );

      setTimeout( () => {
        expect( global.spy ).toHaveBeenCalledTimes( 0 );
        done();
      }, 200 );
    } );

  } );

  describe( 'scrollY', () => {

    it( 'should return the correct browser method', () => {
      expect( typeof utils.scrollY ).toBe( 'function' );
      expect( utils.scrollY() ).toBeGreaterThanOrEqual( 0 );
    } );

  } );

  describe( 'Y location getter', () => {

    beforeEach( () => {
      // Load HTML fixture
      document.body.innerHTML = HTML_SNIPPET1;
    } );

    it( 'should return the correct browser method', () => {
      const el = document.querySelector( '#Interp-1' );
      expect( utils.getYLocation( el ) ).toEqual( -30 );
    } );

  } );

  describe( 'get paragraph positions', () => {

    beforeEach( () => {
      // Load HTML fixture
      document.body.innerHTML = HTML_SNIPPET1;
    } );

    it( 'should return the positions of all paragraphs', () => {
      const paragraphs = document.querySelectorAll( '.regdown-block' );
      expect( utils.getParagraphPositions( paragraphs ) ).toEqual(
        [{'id': 'z-14-i', 'position': -30}, {'id': 'c', 'position': -30}, {'id': 'Interp-1', 'position': -30}]
      );
    } );

  } );

  describe( 'update paragraph positions', () => {

    beforeEach( () => {
      // Load HTML fixture
      document.body.innerHTML = HTML_SNIPPET2;
    } );

    it( 'should update and return the positions of all paragraphs', () => {
      expect( utils.updateParagraphPositions() ).toEqual(
        [{'id': 'e', 'position': -30}, {'id': 'd', 'position': -30}, {'id': 'c', 'position': -30}, {'id': 'b', 'position': -30}, {'id': 'a', 'position': -30}]
      );
    } );

  } );

  describe( 'paragraph getter', () => {

    const paragraphs = [{'id': 'three', 'position': 30}, {'id': 'two', 'position': 20}, {'id': 'one', 'position': 10}];

    it( 'should get paragraph closest to viewport', () => {
      expect( utils.getCurrentParagraph( 'sandwich', paragraphs ) ).toEqual( null );
      expect( utils.getCurrentParagraph( -1, paragraphs ) ).toEqual( null );
      expect( utils.getCurrentParagraph( 0, paragraphs ) ).toEqual( null );
      expect( utils.getCurrentParagraph( 5, paragraphs ) ).toEqual( null );
      expect( utils.getCurrentParagraph( 8, paragraphs ) ).toEqual( null );
      expect( utils.getCurrentParagraph( 0, paragraphs ) ).toEqual( null );
      expect( utils.getCurrentParagraph( 12, paragraphs ) ).toEqual( 'one' );
      expect( utils.getCurrentParagraph( 15, paragraphs ) ).toEqual( 'one' );
      expect( utils.getCurrentParagraph( 19, paragraphs ) ).toEqual( 'one' );
      expect( utils.getCurrentParagraph( 20, paragraphs ) ).toEqual( 'one' );
      expect( utils.getCurrentParagraph( 21, paragraphs ) ).toEqual( 'two' );
      expect( utils.getCurrentParagraph( 30, paragraphs ) ).toEqual( 'two' );
      expect( utils.getCurrentParagraph( 31, paragraphs ) ).toEqual( 'three' );
      expect( utils.getCurrentParagraph( 45, paragraphs ) ).toEqual( 'three' );
      expect( utils.getCurrentParagraph( 73648576, paragraphs ) ).toEqual( 'three' );
    } );

  } );

  describe( 'URL hash updater', () => {

    it( 'should update add the paragraph ID to the URL', () => {
      global.history.replaceState = jest.fn();

      document.body.innerHTML = HTML_SNIPPET1;
      utils.updateParagraphPositions();
      utils.updateUrlHash();
      expect( global.history.replaceState ).toBeCalledWith( null, null, '#z-14-i' );

      document.body.innerHTML = HTML_SNIPPET2;
      utils.updateParagraphPositions();
      utils.updateUrlHash();
      expect( global.history.replaceState ).toBeCalledWith( null, null, '#e' );
    } );

  } );

} );
