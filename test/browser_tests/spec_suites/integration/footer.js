'use strict';

var Footer = require( '../../shared_objects/footer.js' );

describe( 'Footer', function() {
  var _sharedObject;

  var _footerLinkLookup = {
    '/accessibility/':
      'accessibility',
    '/office-civil-rights/':
      'office of civil rights',
    '/office-civil-rights/no-fear-act/':
      'no fear act data',
    '/about-us/careers/':
      'careers',
    '/foia-requests/':
      'foia',
    '/cfpb-ombudsman/':
      'cfpb ombudsman',
    '/about-us/contact-us/':
      'contact us',
    '/about-us/newsroom/':
      'newsroom',
    '/open-government/':
      'open government',
    '/plain-writing/':
      'plain writing',
    '/privacy/':
      'privacy, policy & legal notices',
    '/privacy/website-privacy-policy/':
      'website privacy policy',
    '/tribal/':
      'tribal',
    'http://usa.gov/':
      'usa.gov',
    'http://www.federalreserve.gov/oig/default.htm':
      'office of inspector general',
    'https://facebook.com/cfpb':
      'visit us on facebook',
    'https://twitter.com/cfpb':
      'visit us on twitter',
    'https://www.youtube.com/user/cfpbvideo':
      'visit us on youtube',
    'https://www.flickr.com/photos/cfpbphotos':
      'visit us on flickr',
    'https://www.linkedin.com/company/consumer-financial-protection-bureau':
      'visit us on linkedin'
  };

  beforeAll( function() {
    _sharedObject = new Footer();
    _sharedObject.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( _sharedObject.footer.isPresent() ).toBe( true );
  } );

  it( 'should include navList', function() {
    expect( _sharedObject.navList.isPresent() ).toBe( true );
  } );

  it( 'should include links and links should be valid', function() {
    var _baseURL;
    var _linkHref;
    var _linkText;

    browser.getCurrentUrl().then( function( urlValue ) {
      _baseURL = urlValue.substring( 0, urlValue.length - 1 );
    } );

    expect( _sharedObject.links.count() ).toBeGreaterThan( 0 );

    _sharedObject.links.each( function( element ) {
      element.getAttribute( 'href' ).then( function( hrefValue ) {
        _linkHref = ( hrefValue || '' ).replace( _baseURL, '' );
        expect( _footerLinkLookup.hasOwnProperty( _linkHref ) ).toBe( true );
      } );

      element.getText().then( function( textValue ) {
        _linkText = textValue.toLowerCase();
        expect( _footerLinkLookup[_linkHref] ).toContain( _linkText );
      } );

    } );

  } );

  it( 'should include post', function() {
    expect( _sharedObject.post.isPresent() ).toBe( true );
  } );

  it( 'should include officialWebsite', function() {
    expect( _sharedObject.officialWebsite.isPresent() ).toBe( true );
  } );

} );
