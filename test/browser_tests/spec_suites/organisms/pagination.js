'use strict';

var Blog = require(
    '../../page_objects/page_blog.js'
  );

describe( 'Pagination', function() {
  var page;

  beforeEach( function() {
    page = new Blog();
    page.get();
  } );

  it( 'should navigate to the second page', function() {
    page.paginationNextBtn.click();
    browser.sleep( 1000 );

    expect( browser.getCurrentUrl() ).toContain( 'page=2' );
  } );

  it( 'should navigate to the first page', function() {
    page.paginationNextBtn.click();
    browser.sleep( 1000 );

    page.paginationPrevBtn.click();
    browser.sleep( 1000 );

    expect( browser.getCurrentUrl() ).toContain( 'page=1' );
  } );

  it( 'should navigate to the fifth page', function() {
    page.paginationPageInput.sendKeys( '5' );
    page.paginationPageBtn.click();
    browser.sleep( 1000 );

    expect( browser.getCurrentUrl() ).toContain( 'page=5' );
  } );
} );
