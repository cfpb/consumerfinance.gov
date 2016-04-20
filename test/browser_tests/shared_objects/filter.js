'use strict';

var _searchFilter =
  element( by.css( '.o-filterable-list-controls .m-expandable' ) );

function _getFilterElement( selector ) {
  return _searchFilter.element( by.css( selector ) );
}

var filter = {
  searchFilter: _searchFilter,

  searchFilterBtn: _getFilterElement( '.m-expandable_target' ),

  searchFilterShowBtn: _getFilterElement( '.m-expandable_cue-open' ),

  searchFilterHideBtn: _getFilterElement( '.m-expandable_cue-close' ),

  searchFilterSubmitBtn: _getFilterElement( 'btn[type="submit"]' )

};

module.exports = filter;
