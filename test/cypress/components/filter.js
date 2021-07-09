export class Filter {

  apply() {
    return cy.get( 'form[action="."]' ).submit();
  }

  clear() {
    cy.get( '.a-btn__warning' ).click( { force: true } );
  }

  typeAheadLanguage( name ) {
    return cy.get( `#o-filterable-list-controls_language` ).type( name );
  }

  clickLanguage( name ) {
    cy.get( '#o-filterable-list-controls_language' ).click();
    return cy.get( `label[for="language-${ name }"]` )
      .scrollIntoView()
      .click();
  }

  checkArchivedItem( name ) {
    return cy.get( `#filter_archived_${ name }"]` ).check( { force: true } );
  }

  checkCategoryId( id ) {
    return cy.get( `#filter_categories_${ id }` ).check( { force: true } );
  }

  categoryLabel( id ) {
    return cy.get( `label[for="filter_categories_${ id }"]` );
  }

  checkCategoryName( name ) {
    return this.checkCategoryId( name.split( ' ' ).join( '-' ).toLowerCase() );
  }

  clickCategory( name ) {
    const category = name.split( ' ' ).join( '-' ).toLowerCase();
    return cy.get( `#categories-${ category }` ).click( { force: true } );
  }

  typeAheadTopic( name ) {
    return cy.get( `#o-filterable-list-controls_topics` ).type( name );
  }

  clickTopic( name ) {
    const topic = name.split( ' ' ).join( '-' ).toLowerCase();
    cy.get( '#o-filterable-list-controls_topics' ).click();
    return cy.get( `label[for="topics-${ topic }"]` )
      .scrollIntoView()
      .click();
  }

  expandable() {
    return cy.get( '.o-expandable' );
  }

  expandableCue( name ) {
    return cy.get( `.o-expandable_cue .o-expandable_cue-${ name }` );
  }

  expandableTarget() {
    return cy.get( '.o-expandable_target' );
  }

  search() {
    return cy.get( '.o-expandable_header .o-expandable_target' );
  }

  open() {
    return this.expandableCue( 'open' ).click();
  }

  close() {
    return this.expandableCue( 'close' ).click();
  }

  show() {
    return this.expandableTarget().first().click();
  }

  hide() {
    return this.expandableTarget().last().click();
  }

}
