import {
  CreditCardAgreementSearch
} from '../../../pages/data-research/credit-card-agreements-search';

const searchPage = new CreditCardAgreementSearch();

describe( 'Credit Card Agreements Search', () => {

  it( 'should render agreements for a selected lender', () => {
    searchPage.open();
    searchPage.selectIssuer( 'Bank of America' );
    searchPage.agreementsList().should( 'be.visible' );
    searchPage.agreementsList().should( 'contain', 'Bank of America' );
  } );

} );
