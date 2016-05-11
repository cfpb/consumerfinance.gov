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

  searchCategoryLabel: _getFilterElement(
    'label[for="filter1_categories_at-the-cfpb"]'
  ),

  searchFilterSubmitBtn: _getFilterElement( 'input[type="submit"]' )
};

module.exports = filter;
