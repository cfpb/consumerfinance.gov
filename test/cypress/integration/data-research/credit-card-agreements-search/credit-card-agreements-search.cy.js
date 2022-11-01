import { CreditCardAgreementSearch } from './credit-card-agreements-search-helpers.cy.js';

const searchPage = new CreditCardAgreementSearch();

describe('Credit Card Agreements Search', () => {
  it('should render agreements for a selected lender', () => {
    searchPage.open();
    searchPage.getIssuer().then((issuer) => {
      searchPage.selectIssuer(issuer.get(0).innerText);
      searchPage.agreementsList().should('be.visible');
      searchPage.agreementsList().should('contain', issuer.get(0).innerText);
    });
  });
});
