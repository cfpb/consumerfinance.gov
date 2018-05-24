const _oFilterableListControls =
  element( by.css( '.o-filterable-list-controls' ) );
const multiselect = require( '../shared_objects/multi-select' );
const EC = protractor.ExpectedConditions;


function _getFilterableElement( selector ) {
  return _oFilterableListControls.element( by.css( selector ) );
}

async function open() {
  const expandable = this.mExpandable;
  await expandable.click();

  return browser.wait( EC.elementToBeClickable( expandable ) );
}

function close() {
  return this.mExpandable.click();
}

const oFilterableListControls = {
  mExpandable:   _getFilterableElement( '.o-expandable' ),
  mNotification: _getFilterableElement( '.m-notification' ),
  oPostPreview:  _getFilterableElement( '.o-post-preview' ),
  open:          open,
  close:         close
};

Object.assign( oFilterableListControls, multiselect );

module.exports = oFilterableListControls;
