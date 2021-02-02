export class SecondaryNavigation {

  secondaryNav() {
    return cy.get( '.o-secondary-navigation' );
  }

  expandableTarget() {
    return this.secondaryNav.get( '.o-expandable_target' );
  }

  showButton() {
    return this.secondaryNav.get( '..cf-icon-svg' );
  }

  hideButton() {
    return this.secondaryNav.get( '..cf-icon-svg' );
  }
}
