'use strict';

var Blog = require(
    '../../page_objects/sublanding_filterable_page.js'
  );

describe( 'Multiselect', function() {
  var page;

  beforeEach( function() {
    page = new Blog();
    page.get();

    page.searchFilterBtn.click();
    browser.sleep( 1000 );
  } );

  describe( 'on page load', function() {
    it( 'should create the multiselect', function() {
      expect( page.multiSelect.isDisplayed() ).toBe( true );
    } );

    it( 'should not show the dropdown', function() {
      expect( page.multiSelectFieldset.isDisplayed() ).toBe( false );
    } );
  } );

  describe( 'when interacting with search input', function() {
    it( 'should show the dropdown on click', function() {
      page.multiSelectSearch.click();
      browser.sleep( 1000 );

      expect( page.multiSelectFieldset.isDisplayed() ).toBe( true );
    } );

    xit( 'should show the dropdown on focus', function() {
      // Couldn't get this to tab over, not sure why
      var prevInput = browser.element(
        by.css( 'label[for="filter1_categories_info-for-consumers"]' )
      );
      prevInput.click();
      browser.sleep( 1000 );
      prevInput.sendKeys( protractor.Key.TAB );
      browser.sleep( 1000 );

      expect( page.multiSelectFieldset.isDisplayed() ).toBe( true );
    } );

    it( 'should hide the dropdown when losing focus', function() {
      page.multiSelectSearch.click();
      browser.sleep( 1000 );
      page.multiSelectSearch.sendKeys( protractor.Key.TAB );
      browser.sleep( 1000 );

      expect( page.multiSelectFieldset.isDisplayed() ).toBe( false );
    } );
  } );

  describe( 'when typing in search input', function() {
    it( 'should return the matched results', function() {
      page.multiSelectSearch.sendKeys( 'students' );
      browser.sleep( 1000 );

      var results = browser.element
        .all( by.css( '.cf-multi-select .filter-match' ) );

      expect( results.count() ).toBe( 1 );
      expect( results.first().getAttribute( 'data-option' ) )
        .toContain( 'students' );
      expect( page.multiSelectOptions.getAttribute( 'class' ) )
        .toContain( 'filtered' );
    } );

    it( 'should not return the unmatched results', function() {
      page.multiSelectSearch.sendKeys( 'students' );
      browser.sleep( 1000 );

      var results = browser.element
        .all( by.css( '.cf-multi-select .filter-match' ) );

      expect( results.first().getAttribute( 'data-option' ) )
        .not.toContain( 'Mortgages' );
    } );

    it( 'should clear the input and close the results', function() {
      page.multiSelectSearch.sendKeys( 'students' );
      browser.sleep( 1000 );
      page.multiSelectSearch.sendKeys( protractor.Key.ESCAPE );

      var results = browser.element
        .all( by.css( '.cf-multi-select .filter-match' ) );

      expect( results.count() ).toBe( 0 );
      expect( page.multiSelectOptions.getAttribute( 'class' ) )
        .not.toContain( 'filtered' );
      expect( page.multiSelectFieldset.isDisplayed() ).toBe( false );
    } );

    it( 'should highlight the first item', function() {
      page.multiSelectSearch.click();
      browser.sleep( 1000 );
      page.multiSelectSearch.sendKeys( protractor.Key.ARROW_DOWN );

      var results = browser.element
        .all( by.css( '.cf-multi-select_options li input' ) );

      expect( results.first().getText() )
        .toBe( browser.driver.switchTo().activeElement().getText() );
    } );
  } );

  describe( 'when interacting with options list', function() {
    var options = browser.element
        .all( by.css( '.cf-multi-select_label' ) );
    var choices;

    it( 'should add an option to choices list when clicked', function() {
      page.multiSelectSearch.click();
      browser.sleep( 1000 );

      options.first().click();
      browser.sleep( 1000 );

      choices = browser.element
        .all( by.css( '.cf-multi-select_choices label' ) );

      expect( choices.count() ).toBe( 1 );
      expect( choices.first().getText() ).toContain( 'Mortgages' );
    } );

    it( 'should remove an option from choices when clicked', function() {
      page.multiSelectSearch.click();
      browser.sleep( 1000 );

      options.first().click();
      browser.sleep( 500 );
      options.first().click();
      browser.sleep( 1000 );

      choices = browser.element
        .all( by.css( '.cf-multi-select_choices label' ) );

      expect( choices.count() ).toBe( 0 );
    } );

    xit( 'should add an option with RETURN key', function() {
      // Current bug, needs to be fixed. Checks item but doesn't
      // add it to the choices list
      page.multiSelectSearch.click();
      browser.sleep( 1000 );
      page.multiSelectSearch.sendKeys( protractor.Key.ARROW_DOWN );

      browser.driver.switchTo().activeElement()
        .sendKeys( protractor.Key.RETURN );
      browser.sleep( 1000 );

      choices = browser.element
        .all( by.css( '.cf-multi-select_choices label' ) );

      expect( choices.count() ).toBe( 1 );
      expect( choices.first().getText() ).toContain( 'Mortgages' );
    } );

    xit( 'should remove an option with RETURN key', function() {
       // Current bug, needs to be fixed. Checks item but doesn't
      // add it to the choices list
      page.multiSelectSearch.click();
      browser.sleep( 1000 );
      page.multiSelectSearch.sendKeys( protractor.Key.ARROW_DOWN );

      browser.driver.switchTo().activeElement()
        .sendKeys( protractor.Key.RETURN );
      browser.sleep( 1000 );
      browser.driver.switchTo().activeElement()
        .sendKeys( protractor.Key.RETURN );

      choices = browser.element
        .all( by.css( '.cf-multi-select_choices label' ) );

      expect( choices.count() ).toBe( 0 );
    } );
  } );

  describe( 'when interacting with choices list', function() {
    var options = browser.element
        .all( by.css( '.cf-multi-select_label' ) );
    var choices;

    it( 'should remove option from choices when clicked', function() {
      page.multiSelectSearch.click();
      browser.sleep( 1000 );

      options.first().click();
      browser.sleep( 1000 );

      choices = browser.element
        .all( by.css( '.cf-multi-select_choices label' ) );

      choices.first().click();
      browser.sleep( 1000 );

      choices = browser.element
        .all( by.css( '.cf-multi-select_choices label' ) );

      expect( choices.count() ).toBe( 0 );
    } );
  } );
} );
