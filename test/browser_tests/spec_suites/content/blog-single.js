'use strict';

var BlogSingle = require(
    '../../page_objects/page_blog-single.js'
  );

describe( 'The Blog single Page', function() {
  var page;

  beforeAll( function() {
    page = new BlogSingle();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Lessons we’ve learned' );
  } );

  it( 'should include a post title', function() {
    expect( page.postTitle.getText() ).toBe( 'Lessons we’ve learned' );
  } );

  it( 'should include a post byline', function() {
    expect( page.postByLine.isPresent() ).toBe( true );
  } );

  it( 'should include a post body', function() {
    expect( page.postByLine.isPresent() ).toBe( true );
  } );

  it( 'should include breadcrumbs', function() {
    expect( page.breadcrumbs.getText() ).toBe( 'Blog' );
  } );

  it( 'should include tags', function() {
    expect( page.tags.isPresent() ).toBe( true );
  } );

  it( 'should include a content sidebar', function() {
    expect( page.contentSidebar.isPresent() ).toBe( true );
  } );

  it( 'should include a Stay Informed section in the sidebar', function() {
    expect( page.stayInformedSection.isPresent() ).toBe( true );
  } );

  it( 'should include a Stay Informed section title', function() {
    expect( page.stayInformedSectionTitle.getText() ).toBe( 'STAY INFORMED' );
  } );

  it( 'should include an Email Subscribe form', function() {
    expect( page.emailSubscribeForm.isPresent() ).toBe( true );
  } );

  it( 'should include an Email Subscribe label', function() {
    expect( page.emailFormLabel.getText() ).toBe( 'Email Address' );
  } );

  it( 'should include an Email Subscribe input', function() {
    expect( page.emailFormInput.isPresent() ).toBe( true );
    expect( page.emailFormInput.getAttribute( 'placeholder' ) )
    .toBe( 'example@mail.com' );
  } );

  it( 'should include an Email Subscribe hidden field', function() {
    expect( page.emailFormHiddenField.getAttribute( 'value' ) )
    .toBe( 'USCFPB_91' );
    expect( page.emailFormHiddenField.getAttribute( 'name' ) )
    .toBe( 'code' );
  } );

  it( 'should include an Email Subscribe button', function() {
    expect( page.emailFormBtn.getAttribute( 'value' ) )
    .toBe( 'Sign Up' );
  } );

  it( 'should include an RSS Subscribe section', function() {
    expect( page.rssSubscribeSection.isPresent() ).toBe( true );
  } );

  it( 'should include an RSS Subscribe button', function() {
    expect( page.rssSubscribeBtn.getText() ).toContain( 'Subscribe to RSS' );
  } );

} );
