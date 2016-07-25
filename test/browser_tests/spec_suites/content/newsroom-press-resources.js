'use strict';

var PressResources = require(
    '../../page_objects/page_newsroom-press-resources.js'
  );

describe( 'The Newsroom Press Resources Page', function() {
  var page;

  beforeAll( function() {
    page = new PressResources();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Press resources' );
  } );

  it( 'should include a main title', function() {
    expect( page.mainTitle.getText() ).toBe( 'Press Resources' );
  } );

  it( 'should have a side nav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should include a sub title', function() {
    expect( page.subTitle.getText() ).toBe( 'Press contacts' );
  } );

  it( 'should include a Press contact email address', function() {
    expect( page.contactListEmail.getText() )
    .toBe( 'press@consumerfinance.gov' );
    expect( page.contactListEmail.getAttribute( 'href' ) )
    .toBe( 'mailto:press@consumerfinance.gov' );
  } );

  it( 'should include a Press contact list phone number', function() {
    expect( page.contactListPhone.getText() ).toBe( '(202) 435-7170' );
    expect( page.contactListPhone.getAttribute( 'href' ) )
    .toBe( 'tel:2024357170' );
  } );

  it( 'should include a Press section title', function() {
    expect( page.pressSectionTitle.getText() ).toBe( 'Photos and bios' );
  } );

  it( 'should include a Press section intro', function() {
    expect( page.pressSectionIntro.isPresent() ).toBe( true );
  } );

  it( 'should include Director’s bio', function() {
    expect( page.directorsBioLink.getText() ).toBe( 'Biography' );
  } );

  it( 'should include Director’s images', function() {
    expect( page.directorsImage.getAttribute( 'src' ) ).toExist;
    expect( page.directorsHighResImageLink.getText() )
      .toBe( 'High-res portrait' );
    expect( page.directorsLowResImageLink.getText() )
      .toBe( 'Low-res portrait' );
  } );

  it( 'should include Deputy Director’s bio', function() {
    expect( page.deputyDirectorsBioLink.getText() ).toBe( 'Biography' );
  } );

  it( 'should include the Deputy Director’s images', function() {
    expect( page.deputyDirectorsImage.getAttribute( 'src' ) ).toExist;
    expect( page.deputyDirectorsHighResImageLink.getText() )
      .toBe( 'High-res portrait' );
    expect( page.deputyDirectorsLowResImageLink.getText() )
      .toBe( 'Low-res portrait' );

  } );

  it( 'should include a Press section intro', function() {
    expect( page.pressSectionIntro.isPresent() ).toBe( true );
  } );

  it( 'should include more than one contact person', function() {
    expect( page.contactPersons.count() ).toBeGreaterThan( 1 );
  } );

  xit( 'should include a Stay Informed section', function() {
    expect( page.stayInformedSection.isPresent() ).toBe( true );
  } );

  xit( 'should include a Stay Informed section title', function() {
    expect( page.stayInformedSectionTitle.getText() ).toBe( 'STAY INFORMED' );
  } );

  xit( 'should include a Email Subscribe form', function() {
    expect( page.emailSubscribeForm.isPresent() ).toBe( true );
  } );

  xit( 'should include a Email Subscribe label', function() {
    expect( page.emailFormLabel.getText() ).toBe( 'Email address' );
  } );

  xit( 'should include a Email Subscribe input', function() {
    expect( page.emailFormInput.isPresent() ).toBe( true );
    expect( page.emailFormInput.getAttribute( 'placeholder' ) )
    .toBe( 'example@mail.com' );
  } );

  xit( 'should include a Email Subscribe hidden field', function() {
    expect( page.emailFormHiddenField.getAttribute( 'value' ) )
    .toBe( 'USCFPB_23' );
    expect( page.emailFormHiddenField.getAttribute( 'name' ) )
    .toBe( 'code' );
  } );

  xit( 'should include a Email Subscribe button', function() {
    expect( page.emailFormBtn.getAttribute( 'value' ) )
    .toBe( 'Sign up' );
  } );

  xit( 'should include a RSS Subscribe section', function() {
    expect( page.rssSubscribeSection.isPresent() ).toBe( true );
  } );

  xit( 'should include a RSS Subscribe button', function() {
    expect( page.rssSubscribeBtn.getText() ).toBe( 'Subscribe to RSS' );
  } );

} );
