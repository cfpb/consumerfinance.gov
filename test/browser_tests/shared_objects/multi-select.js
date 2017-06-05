'use strict';

var _multiSelect =
  element.all( by.css( '.cf-multi-select' ) ).first();

function _getMultiSelectElement( selector ) {
  return _multiSelect.element( by.css( selector ) );
}

var multiSelect = {
  multiSelect: _multiSelect,

  multiSelectChoices: _getMultiSelectElement( '.cf-multi-select_choices' ),

  multiSelectHeader: _getMultiSelectElement( '.cf-multi-select_header' ),

  multiSelectSearch: _getMultiSelectElement( '.cf-multi-select_search' ),

  multiSelectFieldset: _getMultiSelectElement( '.cf-multi-select_fieldset' ),

  multiSelectOptions: _getMultiSelectElement( '.cf-multi-select_options' )

};

module.exports = multiSelect;
