'use strict';

var _oFilterableListControls =
    element( by.css( '.o-filterable-list-controls' ) );

var multiselect = require( '../shared_objects/multi-select' );
var EC = protractor.ExpectedConditions;



function _getFilterableElement( selector ) {
  return _oFilterableListControls.element( by.css( selector ) );
}

function open() {
  var expandable = this.mExpandable;

  return expandable.click()
         .then( function() {
           return browser.wait( EC.elementToBeClickable( expandable ) );
         } );
}

function close() {
  return this.mExpandable.click();
}

var oFilterableListControls = {
  mExpandable:   _getFilterableElement( '.o-expandable' ),

  mNotification: _getFilterableElement( '.m-notification' ),

  oPostPreview:  _getFilterableElement( '.o-post-preview' ),

  open:          open,

  close:         close
};

Object.assign( oFilterableListControls, multiselect );

module.exports = oFilterableListControls;
