export class Filter {

  apply() {
    return cy.get( 'form[action="."]' ).submit();
  }

  clear() {
    cy.get( '.a-btn__warning' ).click();
  }

  clickAuthor( name ) {
    const author = name.split( ' ' ).join( '-' ).toLowerCase();
    return cy.get( `#authors-${ author }` ).click( { force: true } );
  }

  checkArchivedItem( name ) {
    return cy.get( `#filter_archived_${ name }"]` ).check( { force: true } );
  }

  checkCategoryId( id ) {
    return cy.get( `#filter_categories_${ id }` ).check( { force: true } );
  }

  checkCategoryName( name ) {
    return this.checkCategoryId( name.split( ' ' ).join( '-' ).toLowerCase() );
  }

  clickTopic( name ) {
    const topic = name.split( ' ' ).join( '-' ).toLowerCase();
    return cy.get( `#topics-${ topic }` ).click( { force: true } );
  }

  expandable() {
    return cy.get( '.o-expandable' );
  }

  categoryLabel( id ) {
    return cy.get( `label[for="filter_categories_${ id }"]` );
  }

  searchFilterBtn() {
    return cy.get( '.o-expandable_header .o-expandable_target' );
  }

  searchFilterShowBtn() {
    return cy.get( '.o-expandable_cue .o-expandable_cue-open' );
  }

  searchFilterHideBtn() {
    return cy.get( '.o-expandable_cue .o-expandable_cue-close' );
  }

}
