'use strict';

var _searchFilter = element( by.css( '[data-qa-hook="filter"]' ) );

function _getFilterElement( selector ) {
  return _searchFilter.element( by.css( selector ) );
}

var filter = {
  searchFilter: _searchFilter,

  searchFilterCategories:
  _getFilterElement( '[data-qa-hook="filter-categories"]' ),

  searchFilterBtn: _getFilterElement( '.m-expandable_target' ),

  searchFilterShowBtn: _getFilterElement( '.m-expandable_cue-open' ),

  searchFilterHideBtn: _getFilterElement( '.m-expandable_cue-close' ),

  searchFilterSubmitBtn: _getFilterElement( 'btn[type="submit"]' )

};

module.exports = filter;
