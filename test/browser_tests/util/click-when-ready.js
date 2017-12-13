const EC = protractor.ExpectedConditions;

function _clickElement( element ) {

  return browser
    .wait( EC.elementToBeClickable( element ) )
    .then( element.click );
}

function clickWhenReady( elements ) {

  if ( elements instanceof protractor.ElementFinder ) {
    elements = [ elements ];
  }

  if ( Array.isArray( elements ) === false ) {
    return Promise.resolve();
  }

  return elements.reduce( ( promise, element ) =>
    promise.then( _clickElement.bind( null, element ) ), Promise.resolve()
  );
}

module.exports = clickWhenReady;
