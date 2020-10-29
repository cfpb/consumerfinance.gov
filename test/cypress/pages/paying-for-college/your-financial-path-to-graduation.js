export class PfcFinancialPathToGraduation {

  open() {
    cy.visit( '/paying-for-college/your-financial-path-to-graduation/' );
  }

  click( button_text ) {
    cy.get( '.a-btn' ).contains( `${ button_text }` ).click();
  }

  setText( name, value ) {
    cy.get( `#${ name }` ).type( value );
  }

  selectProgram( program, type ) {
    cy.get( `#program-${ program }-radio_${ type }` ).check( { force: true } );
  }

  affordLoanChoice( name ) {
    cy.get( `#affording-loans-choices_${ name }` ).check( { force: true } );
  }

  actionPlan( name ) {
    cy.get( `#action-plan_${ name }` ).check( { force: true } );
  }
}
