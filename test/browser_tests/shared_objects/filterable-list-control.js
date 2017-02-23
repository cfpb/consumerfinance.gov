'use strict';

var _oFilterableListControls =
  element( by.css( '.o-filterable-list-controls' ) );

function _getFilterableElement( selector ) {
  return _oFilterableListControls.element( by.css( selector ) );
}

var oFilterableListControls = {
  mExpandable: _getFilterableElement( '.o-expandable' ),

  mNotification: _getFilterableElement( '.m-notification' ),

  oPostPreview: _getFilterableElement( '.o-post-preview' )
};

module.exports = oFilterableListControls;
