import "core-js/stable";
import "regenerator-runtime/runtime";

const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/paying-for-college';
const chartView = require( `${ BASE_JS_PATH }/js/views/chart-view.js` ).chartView;
const constantsModel = require( `${ BASE_JS_PATH }/js/models/constants-model.js` ).constantsModel;
const expensesModel = require( `${ BASE_JS_PATH }/js/models/expenses-model.js` ).expensesModel;
const expensesView = require( `${ BASE_JS_PATH }/js/views/expenses-view.js` ).expensesView;
const financialModel = require( `${ BASE_JS_PATH }/js/models/financial-model.js` ).financialModel;
const financialView = require( `${ BASE_JS_PATH }/js/views/financial-view.js` ).financialView;
const getApiValues = require( `${ BASE_JS_PATH }/js/dispatchers/get-api-values.js` );
const getModelValues = require( `${ BASE_JS_PATH }/js/dispatchers/get-model-values.js` );
const schoolModel = require( `${ BASE_JS_PATH }/js/models/school-model.js` ).schoolModel
const stateModel = require( `${ BASE_JS_PATH }/js/models/state-model.js` ).stateModel;
const updateModels = require( `${ BASE_JS_PATH }/js/dispatchers/update-models.js` );
const updateState = require( `${ BASE_JS_PATH }/js/dispatchers/update-state.js` ).updateState;
const updateView = require( `${ BASE_JS_PATH }/js/dispatchers/update-view.js` );

const createXHRMock = data => {
  const xhrMock = {
    open: jest.fn(),
    send: jest.fn(),
    readyState: 4,
    status: 200,
    responseText: JSON.stringify( data || {})
  };
  return xhrMock;
};

describe( 'The Cost Tool model dispatchers', () => {

  describe( 'get-model-values', () => {
    it( 'should find the correct value inside the financial model', () => {
      financialModel.values.test = 13;
      expect( getModelValues.getFinancialValue( 'test' ) ).toEqual( 13 );
    } );

    it( 'should find the correct value inside the school model', () => {
      schoolModel.values.test = 23;
      expect( getModelValues.getSchoolValue( 'test' ) ).toEqual( 23 );
    } );

    it( 'should find the correct value inside the constants model', () => {
      constantsModel.values.test = 33;
      expect( getModelValues.getConstantsValue( 'test' ) ).toEqual( 33 );
    } );

  } );

  describe( 'get-state', () => {
  	it( 'should get a value from the state model', () => {
  		stateModel.values.test = 42;
  		expect( getModelValues.getStateValue( 'test' ) ).toEqual( 42 );
  	} );
  } );

  describe( 'update-models', () => {
  	it( 'should update the financial model via updateFinancial()', () => {
  		// We should have to create the Financial Property first
  		financialModel.values.foo = 0;
  		updateModels.updateFinancial( 'foo', 13 );
  		expect( financialModel.values.foo ).toEqual( 13 );
  	} );

  	it( 'should not update the financial model via updateFinancial() if the property is undefined', () => {
  		// We should have to create the Financial Property first
  		delete financialModel.values.foo;
  		updateModels.updateFinancial( 'foo', 13, false );
  		expect( financialModel.values.foo ).toBeUndefined();
  	} );

    it( 'should create properties via createFinancial()', () => {
      delete financialModel.values.foo;
      updateModels.createFinancial( 'foo' );
      expect( financialModel.values.foo ).toEqual( 0 );
    } );

    it( 'should call financialModel recalculation via recalculateFinancials()', () => {
      financialModel.values.dirCost_foo = 25;
      financialModel.values.dirCost_bar = 13;
      updateModels.recalculateFinancials();
      expect( financialModel.values.total_directCosts ).toEqual( 38 );
    } );

    it( 'should update the expenses model via updateExpense()', () => {
      expensesModel.values.doof = 0;
      updateModels.updateExpense( 'doof', 55 );
      expect( expensesModel.values.doof ).toEqual( 55 );
    } );

    it( 'should call expensesModel recalculation via recalculateExpensess()', () => {
      expensesModel.values.item_foo = 22;
      expensesModel.values.item_bar = 99;
      updateModels.recalculateExpenses();
      expect( expensesModel.values.total_expenses ).toEqual( 121 );
    } );

    it( 'should update the schoolModel using the API data', async () => {
      const xhr = window.XMLHttpRequest;
      const xhrMock = createXHRMock();
      window.XMLHttpRequest = jest.fn( () => xhrMock );
      schoolModel.values.school = 'a';
      xhrMock.responseText = JSON.stringify( {
        books: 10,
        school: 'Foo U'
      } );

      const promise = updateModels.updateSchoolData( '1' )

      xhrMock.onreadystatechange(); 

      await promise
        .then( response => {
          expect( getModelValues.getSchoolValue( 'school' ) ).toEqual( 'Foo U' );
        } );

      window.XMLHttpRequest = xhr;
    } );

  } );

  describe( 'update-state', () => {
  	it( 'activeSection should change the activeSection', () => {
  		updateState.activeSection( 'test' );
  		expect( stateModel.values.activeSection ).toEqual( 'test' );
  	} );

  	it( 'getStarted should change the gotStarted property', () => {
  		updateState.getStarted( true );
  		expect( stateModel.values.gotStarted ).toEqual( true );
  	} );

  	it( 'byProperty should update a property of the state model', () => {
  		updateState.byProperty( 'test', 999 );
  		expect( stateModel.values.test ).toEqual( 999 );
  	} );

  } );

} );

describe( 'The Cost Tool API getters', () => {

  const xhr = window.XMLHttpRequest;
  let xhrMock;

  beforeEach( () => {
    xhrMock = createXHRMock();
    window.XMLHttpRequest = jest.fn( () => xhrMock );
  } );

  afterEach( () => {
    window.XMLHttpRequest = xhr;
  } );

  describe( 'getSchoolData', () => {

    it( 'should fetch school data', async () => {
      const promise = getApiValues.getSchoolData( '999999' );
      const url = "/paying-for-college2/understanding-your-financial-aid-offer/api/school/999999";
      xhrMock.responseText = JSON.stringify( {
        foo: 'bar'
      } );

      xhrMock.onreadystatechange(); 

      await promise
        .then( response => {
          const data = JSON.parse( response.responseText );
          expect( xhrMock.open ).toBeCalledWith( 'GET',  url, true );
          expect( data.foo ).toEqual( 'bar' );
        } );
    } );

  } );

  describe( 'schoolSearch', () => {

    it( 'should fetch school search results', async () => {
      const promise = getApiValues.schoolSearch( 'foo' );
      const url = "/paying-for-college2/understanding-your-financial-aid-offer/api/search-schools.json?q=foo";
      xhrMock.responseText = JSON.stringify(
        [ { test: 'doof' },
          { foo: 'bar' } ] );

      xhrMock.onreadystatechange(); 

      await promise
        .then( response => {
          const data = JSON.parse( response.responseText );
          expect( xhrMock.open ).toBeCalledWith( 'GET',  url, true );
          expect( data.length ).toEqual( 2 );
        } );
    } );

  } );

  describe( 'getConstants', () => {

    it( 'should fetch constants', async () => {
      const promise = getApiValues.getConstants();
      const url = "/paying-for-college2/understanding-your-financial-aid-offer/api/constants/";
      xhrMock.responseText = JSON.stringify( {
        fooInterest: .055
      } );

      xhrMock.onreadystatechange(); 

      await promise
        .then( response => {
          const data = JSON.parse( response.responseText );
          expect( xhrMock.open ).toBeCalledWith( 'GET',  url, true );
          expect( data.fooInterest ).toEqual( .055 );
        } );
    } );

  } );

  describe( 'getExpenses', () => {

    it( 'should fetch expenses values', async () => {
      const promise = getApiValues.getExpenses();
      const url = "/paying-for-college2/understanding-your-financial-aid-offer/api/expenses/";
      xhrMock.responseText = JSON.stringify( 
        { NE: { housing: 999 },
          SE: { housing: 888 }
        } );

      xhrMock.onreadystatechange(); 

      await promise
        .then( response => {
          const data = JSON.parse( response.responseText );
          expect( xhrMock.open ).toBeCalledWith( 'GET',  url, true );
          expect( data.NE.housing ).toEqual( 999 );
        } );
    } );

  } );

} );

describe( 'updateView', () => {

  it ( 'should update the expense view via updateExpensesView()', () => {
    const tmp = expensesView.updateExpensesView;
    expensesView.updateExpensesView = jest.fn();
    updateView.updateExpensesView();
    expect( expensesView.updateExpensesView.mock.calls.length ).toBe( 1 );
    expensesView.updateExpensesView = tmp;
  } );

  it ( 'should update the financial view via updateFinancialView()', () => {
    const tmp = financialView.updateFinancialView;
    financialView.updateFinancialItems = jest.fn();
    updateView.updateFinancialView();
    expect( financialView.updateFinancialItems.mock.calls.length ).toBe( 1 );
    financialView.updateFinancialItems = tmp;
  } );

  it ( 'should update the cost of borrowing chart via updateCostOfBorrowingChart()', () => {
    const tmp = chartView.updateCostOfBorrowingChart;
    chartView.updateCostOfBorrowingChart = jest.fn();
    updateView.updateCostOfBorrowingChart();
    expect( chartView.updateCostOfBorrowingChart.mock.calls.length ).toBe( 1 );
    chartView.updateCostOfBorrowingChart = tmp;
  } );

  it ( 'should update the make a plan chart via updateMakePlanChart()', () => {
    const tmp = chartView.updateMakePlanChart;
    chartView.updateMakePlanChart = jest.fn();
    updateView.updateMakePlanChart();
    expect( chartView.updateMakePlanChart.mock.calls.length ).toBe( 1 );
    chartView.updateMakePlanChart = tmp;
  } );

  it ( 'should update the max debt chart via updateMaxDebtChart()', () => {
    const tmp = chartView.updateMaxDebtChart;
    chartView.updateMaxDebtChart = jest.fn();
    updateView.updateMaxDebtChart();
    expect( chartView.updateMaxDebtChart.mock.calls.length ).toBe( 1 );
    chartView.updateMaxDebtChart = tmp;
  } );

  it ( 'should update the max debt chart via updateAffordingChart()', () => {
    const tmp = chartView.updateAffordingChart;
    chartView.updateAffordingChart = jest.fn();
    updateView.updateAffordingChart();
    expect( chartView.updateAffordingChart.mock.calls.length ).toBe( 1 );
    chartView.updateAffordingChart = tmp;
  } );

  it ( 'should update the max debt chart via updateGradMeterChart()', () => {
    const tmp = chartView.updateGradMeterChart;
    chartView.updateGradMeterChart = jest.fn();
    updateView.updateGradMeterChart();
    expect( chartView.updateGradMeterChart.mock.calls.length ).toBe( 1 );
    chartView.updateGradMeterChart = tmp;
  } );

  it ( 'should update the max debt chart via updateRepaymentMeterChart()', () => {
    const tmp = chartView.updateRepaymentMeterChart;
    chartView.updateRepaymentMeterChart = jest.fn();
    updateView.updateRepaymentMeterChart();
    expect( chartView.updateRepaymentMeterChart.mock.calls.length ).toBe( 1 );
    chartView.updateRepaymentMeterChart = tmp;
  } );

} );
