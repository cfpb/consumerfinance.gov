export class MegaMenu {

  megaMenu( name ) {
    return cy.get( `.o-mega-menu_${ name }` );
  }

  megaMenuContent( name ) {
    return this.megaMenu( `content-${ name }` );
  }

  content() {
    return this.megaMenu( 'content' ).first();
  }

  trigger() {
    return this.megaMenuContent( '2-alt-trigger' );
  }

  triggerOpen() {
    return this.megaMenu( 'trigger-open' );
  }

  triggerClose() {
    return this.megaMenu( 'trigger-close' );
  }

  focusFirstLink( value ) {
    return this.megaMenuContent( `${ value }-link` ).first().focus();
  }

  focusLastLink( value ) {
    return this.megaMenuContent( `${ value }-link` ).last().focus();
  }

  clickLink( value ) {
    return this.megaMenuContent( `${ value }-link` ).first().click( { force: true } );
  }

  clickTriggerBtn() {
    return this.megaMenu( 'trigger' ).click( { force: true } );
  }

  contentElementItem() {
    return this.megaMenuContent( 'item' );
  }

  contentElementLink() {
    return this.megaMenuContent( 'link' );
  }

  contentElementLists() {
    return this.megaMenuContent( 'lists' );
  }

  contentLink( value ) {
    return this.megaMenuContent( `${ value }-link` );
  }

  contentItem( value ) {
    return this.megaMenuContent( `${ value }-item` );
  }

  contentLists( value ) {
    return this.megaMenuContent( `${ value }-lists` );
  }

  contentValueListGroup( value ) {
    return this.megaMenuContent( `${ value }-list-group` );
  }

  contentOverview( value ) {
    return this.megaMenuContent( `${ value }-overview` );
  }

  contentOverviewLink( value ) {
    return this.megaMenuContent( `${ value }-overview-link` );
  }

  contentWrapper( value ) {
    return this.megaMenuContent( `${ value }-wrapper` );
  }

  tagLine() {
    return cy.get( 'a-tagline' );
  }

  globalEyebrowElement() {
    return cy.get( '.m-global-eyebrow' );
  }

  globalEyebrow( name ) {
    return cy.get( `.m-global-eyebrow_${ name }` );
  }

  globalEyebrowHorizontal() {
    return this.globalEyebrow( '_horizontal' );
  }

  globalEyebrowList() {
    return this.globalEyebrow( '_list' );
  }

  globalEyebrowLanguages() {
    return this.globalEyebrow( 'languages' );
  }

  clickLanguage( name ) {
    return this.globalEyebrowLanguages.type( `/language/${ name }/` ).click( { force: true } );
  }

  tabbing() {
    /* changing focus from one link to another
       is similar to tabbing between elements */
    this.clickTriggerBtn();
    this.focusFirstLink( '1' );
    this.focusLastLink( '1' );
    this.focusFirstLink( '2' );
    this.focusLastLink( '2' );
  }
}
