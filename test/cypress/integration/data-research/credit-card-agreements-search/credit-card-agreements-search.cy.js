import { CreditCardAgreementSearch } from './credit-card-agreements-search-helpers.cy.js';

const searchPage = new CreditCardAgreementSearch();

describe('Credit Card Agreements Search', () => {
  it('should render agreements for a selected lender', () => {
    searchPage.open();
    searchPage.openContainer().then(() => {
      searchPage.agreementsList().should('be.visible');
    });
  });
});
