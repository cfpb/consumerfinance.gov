const _multiSelect = element.all( by.css( '.cf-multiselect' ) ).first();

function _getMultiSelectElement( selector ) {
  return _multiSelect.element( by.css( selector ) );
}

const elements = {
  base:     _multiSelect,
  choices:  _getMultiSelectElement( '.cf-multiselect_choices' ),
  header:   _getMultiSelectElement( '.cf-multiselect_header' ),
  search:   _getMultiSelectElement( '.cf-multiselect_search' ),
  fieldSet: _getMultiSelectElement( '.cf-multiselect_fieldset' ),
  options:  _getMultiSelectElement( '.cf-multiselect_options' )
};

class MultiSelect {

  constructor() {
    this.elements = elements;
    this._selectedTags = [];

    this.addFocusToElement( elements.search );
  }

  addFocusToElement( element ) {

    function _focus() {
      return browser.executeScript(
        'arguments[0].focus()',
        this
      );
    }

    element.focus = _focus.bind( element );
  }

  async areTagSelected() {
    const tagsSelected = this._selectedTags.length;
    const selectedTagsCount = await this.getDisplayedTagElements().count();

    return tagsSelected !== 0 || selectedTagsCount !== 0;
  }

  clearTags() {
    this.selectedTags = [];

    return this.selectedTags;
  }

  async dropDownHasValue( value ) {
    const selector = `li[data-option="${ value }"].filter-match`;
    const selectedTagsCount = await element.all( by.css( selector ) ).count();

    return selectedTagsCount > 0;
  }

  getChoiceElements() {
    return element.all( by.css( '.cf-multiselect_choices label' ) );
  }

  getChoiceElementsCount() {
    return element.all( by.css( '.cf-multiselect_choices label' ) ).count();
  }

  getDropDownCount() {
    return element.all( by.css( '.cf-multiselect .filter-match' ) ).count();
  }

  getDropDownLabelElements() {
    return browser.element.all(
      by.css( '.cf-multiselect_options li .cf-multiselect_label' )
    );
  }

  getDisplayedTagElements() {
    return element.all( by.css( '.cf-multiselect_choices li' ) );
  }

  isRendered() {
    return this.elements.base.isDisplayed();
  }
}

module.exports = MultiSelect;
