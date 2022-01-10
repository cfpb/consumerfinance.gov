export class Multiselect {

  /**
   * @param {string} label - The text within the `<label>` tag of the
   * multiselect you'd like to select. e.g. "Category" or "Topic"
   */
  constructor( label ) {
    this.label = label;
    this.selectedTags = [];
  }

  clickAway() {
    return cy.get( '.o-expandable_content' ).click( { force: true } );
  }

  multiSelect( name ) {
    return cy.contains( 'label[for^=o-filterable-list-controls]', this.label )
      .next( '.o-multiselect' )
      .find( `.o-multiselect_${ name }` );
  }

  choices() {
    return this.multiSelect( 'choices' );
  }

  header() {
    return this.multiSelect( 'header' );
  }

  searchInput() {
    return this.multiSelect( 'search' );
  }

  fieldSet() {
    return this.multiSelect( 'fieldset' );
  }

  optionsField() {
    return this.multiSelect( 'options' );
  }

  clickSearchInput() {
    return this.searchInput().click( { force: true } );
  }

  enterSearchInput( name ) {
    return this.searchInput().clear( { force: true } ).type( name );
  }

  async areTagSelected() {
    const tagsSelected = this.selectedTags.length;
    const selectedTagsCount = await this.displayedTag().length;

    return tagsSelected !== 0 || selectedTagsCount !== 0;
  }

  clearTags() {
    this.selectedTags = [];

    return this.selectedTags;
  }

  dropDownValue( value ) {
    return cy.get( `li[data-option="${ value }"]` );
  }

  async dropDownHasValue( value ) {
    const selector = `li[data-option="${ value }"].u-filter-match`;
    const selectedTagsCount = await cy.get( selector ).length;
    return selectedTagsCount > 0;
  }

  choicesElement() {
    return this.multiSelect( 'choices' ).find( 'label' );
  }

  choicesElementClick() {
    return this.choicesElement().first().click( { force: true } );
  }

  dropDown() {
    return cy.get( '.o-multiselect .u-filter-match' );
  }

  dropDownLabel() {
    return this.multiSelect( 'options' ).find( 'li .o-multiselect_label' );
  }

  firstChoicesElement() {
    this.dropDownLabel().first().invoke( 'text' ).then( $el => {
      const firstLabel = $el.toString();
      this.choicesElement().first().should( 'have.text', firstLabel );
    } );
  }

  dropDownLabelClick() {
    return this.dropDownLabel().first().click( { force: true } );
  }

  displayedTag() {
    return this.multiSelect( 'choices' ).find( 'li' );
  }

  isRendered() {
    return this.multiSelect( 'search' ).should( 'be.visible' );
  }
}
