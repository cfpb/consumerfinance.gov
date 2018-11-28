import Footer from '../../../../cfgov/unprocessed/js/organisms/Footer';

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
    it( 'should return undefined if already initialized', () => {
      footer.init();
      expect( footer.init() ).toBeUndefined();
    } );
  } );
} );
