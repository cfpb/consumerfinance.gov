const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const skipNav = require( BASE_JS_PATH + 'modules/SkipNav' );

import { simulateEvent } from '../../../util/simulate-event';

let skipLink;
let mainEl;


const HTML_SNIPPET = `
  <a href="#main" id="skip-nav">Skip to main content</a>
  <main class="content" id="main">
    <p>Main content area</p>
  </main>
`;

describe( 'SkpNav', () => {
  beforeEach( () => {

    document.body.innerHTML = HTML_SNIPPET;
    skipLink = document.querySelector( '#skip-nav' );
    mainEl = document.querySelector( '#main' );
    skipNav();
    simulateEvent( 'click', skipLink );
  } );

  describe( 'on skip navigation click', () => {
    it( 'should apply a tabindex to the main element', () => {
      expect( mainEl.hasAttribute( 'tabindex' ) ).toStrictEqual( true );
    } );

    it( 'should apply focus to the main element', () => {
      const focusedElement = document.activeElement;
      expect( mainEl ).toStrictEqual( focusedElement );
    } );
  } );

} );
