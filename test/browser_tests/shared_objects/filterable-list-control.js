'use strict';

var _oFilterableListControls =
	element( by.css( '.o-filterable-list-controls' ) );

var _multiselect = require( '../shared_objects/multiselect' );


function _getFilterableElement( selector ) {
  return _oFilterableListControls.element( by.css( selector ) );
}

var oFilterableListControls = {
  mExpandable: _getFilterableElement( '.o-expandable' ),

  mNotification: _getFilterableElement( '.m-notification' ),

  oPostPreview: _getFilterableElement( '.o-post-preview' )
};

Object.assign( oFilterableListControls, _multiselect );

module.exports = oFilterableListControls;
