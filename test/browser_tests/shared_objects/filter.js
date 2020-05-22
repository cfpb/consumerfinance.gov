const _searchFilter =
  element( by.css(
    '.o-filterable-list-controls .o-expandable'
  ) );

function _getFilterElement( selector ) {
  return _searchFilter.element( by.css( selector ) );
}

const filter = {
  searchFilter: _searchFilter,

  searchFilterBtn: _getFilterElement( '.o-expandable_target' ),

  searchFilterShowBtn: _getFilterElement( '.o-expandable_cue-open' ),

  searchFilterHideBtn: _getFilterElement( '.o-expandable_cue-close' ),

  searchCategoryLabel: _getFilterElement(
    'label[for="filter1_categories_at-the-cfpb"]'
  ),

  searchFilterSubmitBtn: _getFilterElement( 'input[type="submit"]' )
};

module.exports = filter;
