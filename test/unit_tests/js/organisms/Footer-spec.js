import Footer from '../../../../cfgov/unprocessed/js/organisms/Footer.js';

let footer;

const HTML_SNIPPET = `
  <section class="o-footer"></section>
`;

describe( 'Footer', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    footer = new Footer( document.querySelector( '.o-footer' ) );
  } );

  describe( 'init()', () => {
    it( 'should return the instance when initialized', () => {
      expect( footer.init() ).toBeInstanceOf( Footer );
      // Check that an instance is returned on the second call.
      expect( footer.init() ).toBeInstanceOf( Footer );
    } );
  } );
} );
