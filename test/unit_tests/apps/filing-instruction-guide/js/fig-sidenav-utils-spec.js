const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/filing-instruction-guide';
const HTML_SNIPPET = require( '../fixtures/sample-fig-page' );

let fig;

describe( 'The Filing Instruction Guide side navigation', () => {
  describe( 'Table of contents', () => {

    beforeEach( () => {
      // Load HTML fixture
      document.body.innerHTML = HTML_SNIPPET;
      fig = require( `${ BASE_JS_PATH }/js/fig-sidenav-utils.js` );
    } );

    it( 'should find the app root', () => {
      expect( fig.appRoot ).toBeTruthy();
    } );

    it( 'should build a list of nav items', () => {
      expect( fig.navItems.size ).toEqual( 40 );
      expect( fig.navItems.get( '#1' ).innerHTML ).toContain( 'What is the FIG?' );
      expect( fig.navItems.get( '#5' ).innerHTML ).toContain( 'Data validation' );
      expect( fig.navItems.get( '#4.2' ).innerHTML ).toContain( 'Application Date' );
    } );

    it( 'should build a list of nav container items', () => {
      expect( fig.navItemContainers.size ).toEqual( 40 );
    } );

    it( 'should have nav items in the same section have the same containers', () => {
      expect( fig.navItemContainers.size ).toEqual( 40 );
      // Test all seven nav sections
      let i = 7;
      while ( i-- ) {
        // Against each of their subsections
        let n = 26;
        while ( n-- ) {
          if ( fig.navItemContainers.get( `#${ i }.${ n }` ) ) {
            expect( fig.navItemContainers.get( `#${ i }` ) ).toEqual( fig.navItemContainers.get( `#${ i }.${ n }` ) );
          }
        }
      }
    } );

    it( 'should highlight nav items', () => {
      fig.highlightNavItem( '#4' );
      expect( fig.navItems.get( '#4' ).outerHTML ).toContain( 'm-nav-link__current' );
      fig.highlightNavItem( '#2' );
      expect( fig.navItems.get( '#2' ).outerHTML ).toContain( 'm-nav-link__current' );
      fig.highlightNavItem( '#5' );
      expect( fig.navItems.get( '#5' ).outerHTML ).toContain( 'm-nav-link__current' );
    } );

    it( 'should unhighlight nav items', () => {
      fig.highlightNavItem( '#4' );
      fig.unHighlightNavItem( '#4' );
      expect( fig.navItems.get( '#4' ).outerHTML ).not.toContain( 'm-nav-link__current' );
      fig.highlightNavItem( '#2' );
      fig.unHighlightNavItem( '#2' );
      expect( fig.navItems.get( '#2' ).outerHTML ).not.toContain( 'm-nav-link__current' );
      fig.highlightNavItem( '#5' );
      fig.unHighlightNavItem( '#5' );
      expect( fig.navItems.get( '#5' ).outerHTML ).not.toContain( 'm-nav-link__current' );
    } );

  } );

} );
