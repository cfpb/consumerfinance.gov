export class ExploreRates {
    constructor() {}

    open() {
        cy.visit('/owning-a-home/explore-rates/')
    }

    selectState(state) {
        cy.get('#location')
          .select(state)
    }
    
    graph() {
      return cy.get('#chart-section')
        .within(() => {
          return cy.get('figure:first');
        });
    }

}

export class Feedback {
  constructor() {}

  open() {
    cy.visit('/owning-a-home/feedback');
  }

  submitComment(comment) {
    cy.get('#comment').type(comment);
    cy.get('.content_main')
      .within(() => {
        cy.get('form').submit();
      });
  }

  successNotification() {
    return cy.get('.content_main')
      .within(() => {
        return cy.get('.m-notification')
      });
  }

}