const MultiSelect = require( '../../shared_objects/multiselect.js' );
const { Then, When, Before } = require( 'cucumber' );
const chai = require( 'chai' );
const expect = chai.expect;
const chaiAsPromised = require( 'chai-as-promised' );
const EC = protractor.ExpectedConditions;

let multiSelect;

chai.use( chaiAsPromised );

Before( function() {
  multiSelect = new MultiSelect();
} );

When( /I (.*) on the multiselect search input/,
  async function( searchInputAction ) {
    await browser.wait( EC.visibilityOf( multiSelect.elements.search ) );
    await multiSelect.elements.search[searchInputAction]();
  }
);

When( /I enter "(.*)" in the search input/,
  function( searchInputText ) {

    return multiSelect.elements.search.sendKeys( searchInputText );
  }
);

When( 'I hit the escape button on the search input', function() {

  return multiSelect.elements.search.sendKeys( protractor.Key.ESCAPE );
} );

When( /I hit the (.*) arrow on the multiselect/,
  function( arrowDirection ) {
    const directionConstant = protractor.Key[arrowDirection.toUpperCase()];

    return multiSelect.elements.search.sendKeys(
      directionConstant
    );
  }
);

When( 'I click on the first choices element',
  function() {

    return multiSelect.getChoiceElements()
      .first()
      .click();
  }
);

When( /I click on the first option in the dropdown(?:\s)?(?:again)?/,
  async function() {
    const firstOption = await multiSelect.getDropDownLabelElements().first();
    await browser.wait( EC.visibilityOf( firstOption ) );

    return firstOption.click();
  }
);

Then( 'the multiselect should be rendered', function() {

  return expect( multiSelect.isRendered() )
    .to.eventually
    .equal( true );
} );

Then( 'no tags should be selected', function() {

  return expect( multiSelect.areTagSelected() )
    .to.eventually
    .equal( false );
} );

Then( /the multiselect dropdown (should|shouldn't) be visible/,
  function( shouldBeVisible ) {
    let dropdownIsDisplayed = true;

    if ( shouldBeVisible === 'shouldn\'t' ) {
      dropdownIsDisplayed = false;
    }

    return expect( multiSelect.elements.fieldSet.isDisplayed() )
      .to.eventually
      .equal( dropdownIsDisplayed );
  }
);

Then( /the multiselect dropdown (should|shouldn't) display "(.*)"/,
  function( shouldBeDisplayed, dropdownValue ) {
    let valueIsDisplayed = true;

    if ( shouldBeDisplayed === 'shouldn\'t' ) {
      valueIsDisplayed = false;
    }

    return expect( multiSelect.dropDownHasValue( dropdownValue ) )
      .to.eventually
      .equal( valueIsDisplayed );
  }
);

Then( /the multiselect dropdown length should be (.*)/,
  function( dropDownLength ) {

    return expect( multiSelect.getDropDownCount() )
      .to.eventually
      .equal( Number( dropDownLength ) );
  }
);

Then( /the (.*) field (should|shouldn't) contain the class (.*)/,
  function( element, shouldContain, className ) {
    const multiSelectElement =
      multiSelect.elements[element].getAttribute( 'class' );

    if ( shouldContain === 'shouldn\'t' ) {

      return expect( multiSelectElement )
        .to.eventually.not.contain( className );
    }

    return expect( multiSelectElement )
      .to.eventually
      .contain( className );
  }
);

Then( 'the first option should be highlighted',
  function() {
    function _getfirstElementText() {

      return multiSelect.getDropDownLabelElements()
        .first()
        .getAttribute( 'for' );
    }

    function _getActiveElementId() {

      return browser
        .driver
        .switchTo()
        .activeElement()
        .getAttribute( 'id' );
    }

    return Promise.all( [ _getfirstElementText(), _getActiveElementId() ] )
      .then( function( [ firstElementText, activeElementId ] ) {

        return expect( firstElementText )
          .to.equal( activeElementId );
      } );
  }
);

Then( 'the choices element should contain the first option',
  async function() {
    const firstElementText =
      await multiSelect.getDropDownLabelElements().first().getText();
    const choicesText =
      await multiSelect.getChoiceElements().first().getText();
    const choicesCount = await multiSelect.getChoiceElements().count();

    expect( choicesCount ).to.equal( 1 );

    return expect( choicesText ).to.contain( firstElementText );
  }
);

Then( /the choices length should be (.*)/,
  function( choicesCount ) {

    return expect( multiSelect.getChoiceElementsCount() )
      .to.eventually
      .equal( Number( choicesCount ) );
  }
);
