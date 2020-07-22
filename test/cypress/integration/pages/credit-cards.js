import { CreditCardAgreementSearch } from '../../pages/credit-cards/agreements-search';

const searchPage = new CreditCardAgreementSearch();

describe( 'Credit Cards', () => {

  describe( 'Agreements Search', () => {

    it( 'should render agreements for a selected lender', () => {
      searchPage.open();
      searchPage.selectIssuer( 'Bank of America' );
      searchPage.agreementsList().should( 'be.visible' );
      searchPage.agreementsList().should( 'contain', 'Bank of America' );
    } );

  } );

} );
