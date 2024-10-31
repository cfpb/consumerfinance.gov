// http://localhost:8000/paying-for-college2/understanding-your-financial-aid-offer/offer/?iped=133465&pid=5287oid=XFOOX&totl=45000&tuit=38976&hous=3000&book=650&tran=500&othr=500&pelg=1500&schg=2000&stag=2000&othg=100&ta=3000&mta=3000&gib=3000&wkst=3000&parl=14000&perl=3000&subl=15000&unsl=2000&ppl=1000&gpl=1000&prvl=3000&prvi=4.55&prvf=1.01&insl=3000&insi=4.55&inst=8

// iped=224776&pid=444

export class DynamicDisclosures {
  programLengthSelect() {
    return cy.get('#estimated-years-attending');
  }

  confirmVerification(forceParam = false) {
    cy.get('a[href="#info-right"]').click({ force: forceParam });
  }

  denyVerification(forceParam = false) {
    cy.get('a[href="#info-wrong"]').click({ force: forceParam });
  }

  stepTwo(forceParam) {
    cy.get('.continue.step .continue__controls button').click({
      force: forceParam,
    });
  }

  typeText(name, value) {
    cy.get(`#${name}`).type(value);
  }

  setText(name, value) {
    cy.get(`#${name}`).clear();
    cy.get(`#${name}`).type(value);
  }
}
