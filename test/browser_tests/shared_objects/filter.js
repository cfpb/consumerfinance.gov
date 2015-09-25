'use strict';

var _searchFilter = element( by.css( '.js-post-filter' ) );

function _getFilterElement( selector ) {
  return _searchFilter.element( by.css( selector ) );
}

var filter = {
  searchFilter: _searchFilter,

  searchFilterCategories:
  _getFilterElement( '[data-qa-hook="filter-categories"]' ),

  searchFilterBtn: _getFilterElement( '.expandable_target' ),

  searchFilterShowBtn: _getFilterElement( '.expandable_cue-open' ),

  searchFilterHideBtn: _getFilterElement( '.expandable_cue-close' ),

  searchFilterResetBtn: _getFilterElement( '.js-form_clear' ),

  searchFilterSubmitBtn: _getFilterElement( 'btn[type="submit"]' )

};

module.exports = filter;
