export class Multiselect {

  constructor( label ) {
    if ( label ) {
      this.el = cy.contains( 'label[for^=o-filterable-list-controls]', label ).next( '.o-multiselect' );
    } else {
      this.el = cy.get( '.o-multiselect' ).first();
    }
    this.selectedTags = [];
  }

  clickAway() {
    return cy.get( '.o-expandable_content' ).click( { force: true } );
  }

  multiSelect( name ) {
    return this.el.find( `.o-multiselect_${ name }` );
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
    return this.el.find( `li[data-option="${ value }"].u-filter-match` );
  }

  async dropDownHasValue( value ) {
    const selector = `li[data-option="${ value }"].u-filter-match`;
    const selectedTagsCount = await this.el.find( selector ).length;
    return selectedTagsCount > 0;
  }

  choicesElement() {
    return this.el.find( '.o-multiselect_choices label' );
  }

  choicesElementClick() {
    return this.choicesElement().first().click( { force: true } );
  }

  dropDown() {
    return this.el.find( '.o-multiselect .u-filter-match' );
  }

  dropDownLabel() {
    return this.el.find( '.o-multiselect_options li .o-multiselect_label' );
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
    return this.el.find( '.o-multiselect_choices li' );
  }

  isRendered() {
    return this.el.should( 'be.visible' );
  }
}
