const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/paying-for-college';

const financialModel = require( `${ BASE_JS_PATH }/js/models/financial-model.js` ).financialModel;

describe( 'The Cost Tool model utilities', () => {

  describe( 'createFinancialProperty', () => {
    it( 'should create a property that doesn\'t exist and set it to 0', () => {
      financialModel.createFinancialProperty( 'foo' );
      expect( financialModel.values.foo ).toEqual( 0 );
    } );

    it( 'should not reset a property that already exists', () => {
      financialModel.values.top = 15;
      financialModel.createFinancialProperty( 'top' );
      expect( financialModel.values.top ).toEqual( 15 );
    } );
  } );

  describe( 'setValue', () => {
    it( 'should set a value of an extant property', () => {
      financialModel.values.fah = 0;
      financialModel.setValue( 'fah', 23 );
      expect( financialModel.values.fah ).toEqual( 23 );
    } );

    it( 'should not create a property that doesn\'t already exist', () => {
      delete financialModel.values.fah;
      financialModel.setValue( 'fah', 12 );
      expect( financialModel.values.fah ).toBeUndefined();
    } );

  } );

  describe( 'extendValues', () => {
    it( 'should extend the values using the data object', () => {
      financialModel.values.strange = 0;
      financialModel.values.charm = 0;
      const data = {
        strange: 5,
        charm: 10
      };
      financialModel.extendValues( data );
      expect( financialModel.values.strange ).toEqual( 5 );
      expect( financialModel.values.charm ).toEqual( 10 );
    } );
  } );

  describe( 'calculateTotals', () => {
    const data = {
      dirCost_a: 15,
      dirCost_b: 3,
      dirCost_c: 10,
      indiCost_a: 3,
      indiCost_b: 5,
      indiCost_c: 1,
      grant_a: 99,
      grant_b: 6,
      grant_c: 15,
      scholarship_a: 13,
      scholarship_b: 3,
      scholarship_c: 5,
      savings_a: 4,
      savings_b: 5,
      savings_c: 10,
      income_a: 33,
      income_b: 22,
      income_c: 11
    };
    // Set up values in object
    for ( const key in data ) {
      financialModel.createFinancialProperty( key );
    }

    // This should invoke calculateTotals()
    financialModel.extendValues( data );

    it( 'should calculate total direct costs', () => {
      expect( financialModel.values.total_directCosts ).toEqual( 28 );
    } );

    it( 'should calculate total indirect costs', () => {
      expect( financialModel.values.total_indirectCosts ).toEqual( 9 );
    } );

    it( 'should calculate total grants', () => {
      expect( financialModel.values.total_grants ).toEqual( 120 );
    } );

    it( 'should calculate total scholarships', () => {
      expect( financialModel.values.total_scholarships ).toEqual( 21 );
    } );

    it( 'should calculate total savings', () => {
      expect( financialModel.values.total_savings ).toEqual( 19 );
    } );

    it( 'should calculate total income', () => {
      expect( financialModel.values.total_income ).toEqual( 66 );
    } );

    it( 'should calculate total costs', () => {
      expect( financialModel.values.total_costs ).toEqual( 37 );
    } );

    it( 'should calculate total grants and scholarships', () => {
      expect( financialModel.values.total_grantsScholarships ).toEqual( 141 );
    } );
  } );
} );
