export class RelatedLinksSection {

  relatedLinksSection() {
    return cy.get( '.related-links' );
  }

  relatedLinks() {
    return this.relatedLinksSection().get( 'a' );
  }

  relatedLinksSectionTitles() {
    return this.relatedLinksSection().get( 'h2' );
  }

  relatedLinksSectionDescriptions() {
    return this.relatedLinksSection().get( '.short-desc' );
  }
}
