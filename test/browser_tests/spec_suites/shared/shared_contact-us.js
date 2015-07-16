var ContactUsPage = require( '../../page_objects/page_contact-us.js' );

describe( 'Beta Contact Page', function() {
  var phoneClass = 'list_link__phone';

  var page;

  beforeEach( function() {
    page = new ContactUsPage();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Contact us' );
  } );

  it( 'should include the Submit a Complaint phone numbers', function() {
    var firstPhone = page.complaintPhone.first();
    var secondPhone = page.complaintPhone.last();

    expect( page.complaintPhone.count() ).toEqual( 2 );
    expect( page.complaintPhone.getAttribute( 'class' ) ).toMatch( phoneClass );
    expect( firstPhone.getText() ).toBe( '(855) 411-CFPB (2372)' );
    expect( firstPhone.getAttribute( 'href' ) ).toBe( 'tel:8554112372' );
    expect( secondPhone.getText() ).toBe( '(855) 729-CFPB (2372) TTY' );
    expect( secondPhone.getAttribute( 'href' ) ).toBe( 'tel:8557292372' );
  } );

// This hasn't been released to beta yet and should fail when testing that url
  it( 'should link to Submit a Complaint page', function() {
    var complaintLink = element( by.partialLinkText( 'Submit a complaint' ) );

    expect( complaintLink.getText() ).toBeDefined();
    expect( complaintLink.getAttribute( 'href' ) ).toMatch( '/complaint/' );
    expect( complaintLink.getAttribute( 'class' ) ).toMatch( 'jump-link__right' );
  } );

  it( 'should include General Inquiries contact details', function() {
    expect( page.giEmail.getText() ).toBeDefined();
    expect( page.giEmail.getAttribute( 'href' ) ).toBe( 'mailto:info@consumerfinance.gov' );
    expect( page.giPhone.getText() ).toBeDefined();
    expect( page.giPhone.getAttribute( 'href' ) ).toBe( 'tel:2024357000' );
    expect( page.giPhone.getAttribute( 'class' ) ).toMatch( phoneClass );
  } );
} );
