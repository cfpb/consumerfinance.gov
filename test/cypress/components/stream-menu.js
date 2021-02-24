export class StreamMenu {

  streamMenu() {
    cy.get( '.stream-menu' ).first();
  }

  getContentElement( name ) {
    return this.streamMenu().get( `.action-add-block-${ name }` );
  }

  callToActionBtn() {
    return this.getContentElement( 'call_to_action' );
  }

  contentBtn() {
    return this.getContentElement( 'content' );
  }

  contentWithAnchorBtn() {
    return this.getContentElement( 'content_with_anchor' );
  }

  emailSignupBtn() {
    return this.getContentElement( 'email_signup' );
  }

  expandableBtn() {
    return this.getContentElement( 'expandable' );
  }

  expandableGroupBtn() {
    return this.getContentElement( 'expandable_group' );
  }

  feedbackBtn() {
    return this.getContentElement( 'feedback' );
  }

  fullWidthTextBtn() {
    return this.getContentElement( 'full_width_text' );
  }

  mediaBtn() {
    return this.getContentElement( 'media' );
  }

  quoteBtn() {
    return this.getContentElement( 'quote' );
  }

  tableBlock() {
    return this.getContentElement( 'table_block' );
  }

  videoPlayerBtn() {
    return this.getContentElement( 'video_player' );
  }

  wellBtn() {
    return this.getContentElement( 'well' );
  }
}
