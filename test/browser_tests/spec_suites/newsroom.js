'use strict';

var Newsroom = require(
    '../page_objects/page_newsroom.js'
  );

describe( 'The Newsroom Page', function() {
  var page;

  beforeAll( function() {
    page = new Newsroom();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Newsroom' );
  } );

  it( 'should include a main title', function() {
    expect( page.mainTitle.getText() ).toBe( 'Newsroom' );
  } );

  it( 'should have a side nav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should include a featured topic', function() {
    expect( page.featuredTopic.isPresent() ).toBe( true );
  } );

  it( 'should include a Stay Informed section in the sidebar', function() {
    expect( page.stayInformedSection.isPresent() ).toBe( true );
  } );

  it( 'should include a Stay Informed section title', function() {
    expect( page.stayInformedSectionTitle.getText() ).toBe( 'STAY INFORMED' );
  } );

  it( 'should include a Email Subscribe form', function() {
    expect( page.emailSubscribeForm.isPresent() ).toBe( true );
  } );

  it( 'should include a Email Subscribe label', function() {
    expect( page.emailFormLabel.getText() ).toBe( 'Email address' );
  } );

  it( 'should include an Email Subscribe input', function() {
    expect( page.emailFormInput.isPresent() ).toBe( true );
    expect( page.emailFormInput.getAttribute( 'placeholder' ) )
    .toBe( 'example@mail.com' );
  } );

  it( 'should include a Email Subscribe hidden field', function() {
    expect( page.emailFormHiddenField.getAttribute( 'value' ) )
    .toBe( 'USCFPB_23' );
    expect( page.emailFormHiddenField.getAttribute( 'name' ) )
    .toBe( 'code' );
  } );

  it( 'should include a Email Subscribe button', function() {
    expect( page.emailFormBtn.getAttribute( 'value' ) )
    .toBe( 'Sign up' );
  } );

  it( 'should include a Email Subscribe description', function() {
    expect( page.emailFormDescription.isPresent() ).toBe( true );
  } );

  it( 'should include a RSS Subscribe section', function() {
    expect( page.rssSubscribeSection.isPresent() ).toBe( true );
  } );

  it( 'should include a RSS Subscribe button', function() {
    expect( page.rssSubscribeBtn.getText() ).toContain( 'Subscribe to RSS' );
  } );

  it( 'should include a search filter', function() {
    expect( page.searchFilter.isPresent() ).toBe( true );
  } );

  it( 'should include a search filter button', function() {
    expect( page.searchFilterBtn.getText() ).toContain( 'posts' );
  } );

  it( 'should include a search filter categories', function() {
    var searchFilterBtn = page.searchFilterBtn;
    var searchFilterCategories = page.searchFilterCategories;
    searchFilterBtn.click();
    browser.sleep( 1000 );
    searchFilterCategories.getText().then( function() {
      searchFilterBtn.click();
      browser.sleep( 1000 );
    } );
  } );

  it( 'should include a visible Show button', function() {
    expect( page.searchFilterShowBtn.isDisplayed() ).toBe( true );
    expect( page.searchFilterShowBtn.getText() ).toBe( 'Show' );
  } );

  it( 'should include a hidden Hide button', function() {
    expect( page.searchFilterHideBtn.isDisplayed() ).toBe( false );
  } );

  it( 'should include pagination results', function() {
    expect( page.paginationResults.count() ).toBeGreaterThan( 0 );
  } );

  it( 'should include pagination form', function() {
    expect( page.paginationForm.isPresent() ).toBe( true );
  } );

  it( 'should include a previous button within the pagination element',
  function() {
    expect( page.paginationPrevBtn.getText() ).toBe( 'Newer' );
  } );

  it( 'should include a next button within the pagination element',
  function() {
    expect( page.paginationNextBtn.getText() ).toBe( 'Older' );
  } );

  it( 'should include a page input with value set to 1', function() {
    expect( page.paginationPageInput.getAttribute( 'value' ) === 1 );
  } );

} );
