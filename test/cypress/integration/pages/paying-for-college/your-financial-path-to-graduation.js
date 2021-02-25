import {
  PfcFinancialPathToGraduation
} from '../../../pages/paying-for-college/your-financial-path-to-graduation.js';

const page = new PfcFinancialPathToGraduation();

describe( 'Paying For College', () => {
  beforeEach( () => {
    cy.visit( '/paying-for-college/your-financial-path-to-graduation/' );
  } );
  describe( 'Your Financial Path To Graduation', () => {
    it( 'American college search should return results', () => {
      page.clickGetStarted( );
      page.enter( 'American' );
      page.searchResults().should( 'be.visible' );
    } );
    it( 'certificate should display total_costs', () => {
      page.clickGetStarted( );
      page.enter( 'Harvard University' );
      page.searchResults().should( 'be.visible' );
      page.clickSearchResult( 'Harvard University' );
      page.selectProgram( 'type', 'certificate' );
      page.selectProgram( 'length', '1' );
      page.selectProgram( 'housing', 'on-campus' );
      page.selectProgram( 'dependency', 'dependent' );
      page.clickNextStep();
      page.click( 'No' );
      page.setText( 'costs__tuition-fees', '50000' );
      page.setText( 'costs__room-board', '25000' );
      page.setText( 'costs__otherDirect-board', '12500' );
      cy.get( '[data-financial-item="total_directCosts"]' )
        .should( 'contain', '$87,500' );
      page.setText( 'costs__books', '7500' );
      page.setText( 'costs__transportation', '5000' );
      page.setText( 'costs__other', '2500' );
      cy.get( '[data-financial-item="total_indirectCosts"]' )
        .should( 'contain', '$15,000' );
      page.setText( 'costs__otherIndirect', '1250' );
      cy.get( '[data-financial-item="total_costs"]' ).each( el => {
        cy.wrap( el ).should( 'contain', '$103,750' );
      } );
    } );
    it( 'associates degree should display total_costs', () => {
      page.clickGetStarted( );
      page.enter( 'Harvard University' );
      page.searchResults().should( 'be.visible' );
      page.clickSearchResult( 'Harvard University' );
      page.selectProgram( 'type', 'associates' );
      page.selectProgram( 'length', '2' );
      page.selectProgram( 'housing', 'off-campus' );
      page.selectProgram( 'dependency', 'dependent' );
      page.clickNextStep( );
      page.click( 'Yes' );
      page.setText( 'costs__tuition-fees', '100000' );
      page.setText( 'costs__room-board', '50000' );
      page.setText( 'costs__otherDirect-board', '25000' );
      cy.get( '[data-financial-item="total_directCosts"]' )
        .should( 'contain', '$175,000' );
      page.setText( 'costs__books', '12500' );
      page.setText( 'costs__transportation', '7500' );
      page.setText( 'costs__other', '5000' );
      cy.get( '[data-financial-item="total_indirectCosts"]' )
        .should( 'contain', '$25,000' );
      page.setText( 'costs__otherIndirect', '2500' );
      cy.get( '[data-financial-item="total_costs"]' ).each( el => {
        cy.wrap( el ).should( 'contain', '$202,500' );
      } );
    } );
    it( 'graduate degree should display total_costs', () => {
      page.clickGetStarted( );
      page.enter( 'Harvard University' );
      page.searchResults().should( 'be.visible' );
      page.clickSearchResult( 'Harvard University' );
      page.selectProgram( 'type', 'graduate' );
      page.selectProgram( 'length', '4' );
      page.selectProgram( 'housing', 'off-campus' );
      page.clickNextStep( );
      page.click( 'No' );
      page.setText( 'costs__tuition-fees', '400000' );
      page.setText( 'costs__room-board', '200000' );
      page.setText( 'costs__otherDirect-board', '100000' );
      cy.get( '[data-financial-item="total_directCosts"]' )
        .should( 'contain', '$700,000' );
      page.setText( 'costs__books', '50000' );
      page.setText( 'costs__transportation', '25000' );
      page.setText( 'costs__other', '12500' );
      cy.get( '[data-financial-item="total_indirectCosts"]' )
        .should( 'contain', '$87,500' );
      page.setText( 'costs__otherIndirect', '10000' );
      cy.get( '[data-financial-item="total_costs"]' ).each( el => {
        cy.wrap( el ).should( 'contain', '$797,500' );
      } );
      page.clickNextStep( );
      page.setText( 'grants__pell', '9000' );
      page.setText( 'grants__seog', '10000' );
      page.setText( 'grants__otherFederal', '11000' );
      page.setText( 'grants__state', '12000' );
      page.setText( 'grants__school', '13000' );
      page.setText( 'grants__other', '14000' );
      page.setText( 'grants__mta', '4500' );
      page.setText( 'grants__gibill', '15000' );
      page.setText( 'grants_serviceOther', '16000' );
      page.setText( 'scholarships__state', '17000' );
      page.setText( 'scholarships__school', '18000' );
      page.setText( 'scholarships__other', '19000' );
      cy.get( '[data-financial-item="total_grantsScholarships"]' )
        .should( 'contain', '$158,500' );
      page.clickNextStep( );
      page.setText( 'workStudy__workStudy', '50000' );
      cy.get( '[data-financial-item="total_workStudy"]' )
        .should( 'contain', '$50,000' );
      page.clickNextStep( );
      page.setText( 'loans__directUnsub', '2000' );
      cy.get( '[data-financial-item="total_fedLoans"]' )
        .should( 'contain', '$1,979' );
      page.clickNextStep( );
      page.setText( 'loans__stateLoan', '100000' );
      page.setText( 'loans__stateLoanRate', '9' );
      page.setText( 'loans__stateLoanFee', '8' );
      page.setText( 'loans__schoolLoan', '70000' );
      page.setText( 'loans__schoolLoanRate', '6' );
      page.setText( 'loans__schoolLoanFee', '5' );
      page.setText( 'loans__nonprofitLoan', '40000' );
      page.setText( 'loans__nonprofitLoanRate', '3' );
      page.setText( 'loans__nonprofitLoanFee', '2' );
      cy.get( '[data-financial-item="total_publicLoans"]' )
        .should( 'contain', '$197,700' );
      page.clickNextStep( );
      page.setText( 'savings__personal', '10000' );
      page.setText( 'savings__family', '20000' );
      page.setText( 'savings__collegeSavings', '30000' );
      page.setText( 'income__jobOffCampus', '40000' );
      page.setText( 'income__jobOnCampus', '50000' );
      page.setText( 'income__employerAssist', '60000' );
      page.setText( 'income_otherFunding', '70000' );
      cy.get( '[data-financial-item="total_otherResources"]' )
        .should( 'contain', '$280,000' );
      page.clickNextStep( );
      page.clickNextStep( );
      page.clickNextStep( );
      page.clickNextStep( );
      page.clickNextStep( );
      page.affordLoanChoice( 'monthly' );
      page.clickNextStep( );
      page.clickNextStep( );
      page.clickNextStep( );
      page.actionPlan( 'put-into-action' );
      page.clickNextStep( );
    } );
    it( 'bachelors degree should display total_costs', () => {
      page.clickGetStarted( );
      page.enter( 'Harvard University' );
      page.searchResults().should( 'be.visible' );
      page.clickSearchResult( 'Harvard University' );
      page.selectProgram( 'type', 'bachelors' );
      page.selectProgram( 'length', '3' );
      page.selectProgram( 'housing', 'on-campus' );
      page.selectProgram( 'dependency', 'dependent' );
      page.clickNextStep( );
      page.click( 'Yes' );
      page.setText( 'costs__tuition-fees', '200000' );
      page.setText( 'costs__room-board', '100000' );
      page.setText( 'costs__otherDirect-board', '50000' );
      cy.get( '[data-financial-item="total_directCosts"]' )
        .should( 'contain', '$350,000' );
      page.setText( 'costs__books', '25000' );
      page.setText( 'costs__transportation', '12500' );
      page.setText( 'costs__other', '7500' );
      cy.get( '[data-financial-item="total_indirectCosts"]' )
        .should( 'contain', '$45,000' );
      page.setText( 'costs__otherIndirect', '5000' );
      cy.get( '[data-financial-item="total_costs"]' ).each( el => {
        cy.wrap( el ).should( 'contain', '$400,000' );
      } );
      page.clickNextStep( );
      page.setText( 'grants__pell', '9293' );
      page.setText( 'grants__seog', '8000' );
      page.setText( 'grants__otherFederal', '7000' );
      page.setText( 'grants__state', '6000' );
      page.setText( 'grants__school', '5000' );
      page.setText( 'grants__other', '4000' );
      page.setText( 'grants__mta', '4500' );
      page.setText( 'grants__gibill', '3000' );
      page.setText( 'grants_serviceOther', '2000' );
      page.setText( 'scholarships__state', '1000' );
      page.setText( 'scholarships__school', '2000' );
      page.setText( 'scholarships__other', '3000' );
      cy.get( '[data-financial-item="total_grantsScholarships"]' )
        .should( 'contain', '$54,793' );
      page.clickNextStep( );
      page.setText( 'workStudy__workStudy', '50000' );
      cy.get( '[data-financial-item="total_workStudy"]' )
        .should( 'contain', '$50,000' );
      page.clickNextStep( );
      page.setText( 'loans__directUnsub', '2000' );
      cy.get( '[data-financial-item="total_fedLoans"]' )
        .should( 'contain', '$1,979' );
      page.clickNextStep( );
      page.setText( 'loans__stateLoan', '100000' );
      page.setText( 'loans__stateLoanRate', '9' );
      page.setText( 'loans__stateLoanFee', '8' );
      page.setText( 'loans__schoolLoan', '70000' );
      page.setText( 'loans__schoolLoanRate', '6' );
      page.setText( 'loans__schoolLoanFee', '5' );
      page.setText( 'loans__nonprofitLoan', '40000' );
      page.setText( 'loans__nonprofitLoanRate', '3' );
      page.setText( 'loans__nonprofitLoanFee', '2' );
      cy.get( '[data-financial-item="total_publicLoans"]' )
        .should( 'contain', '$197,700' );
      page.clickNextStep( );
      page.setText( 'savings__personal', '10000' );
      page.setText( 'savings__family', '20000' );
      page.setText( 'savings__collegeSavings', '30000' );
      page.setText( 'income__jobOffCampus', '40000' );
      page.setText( 'income__jobOnCampus', '50000' );
      page.setText( 'income__employerAssist', '60000' );
      page.setText( 'income_otherFunding', '70000' );
      cy.get( '[data-financial-item="total_otherResources"]' )
        .should( 'contain', '$280,000' );
      page.clickNextStep( );
      page.clickNextStep( );
      page.clickNextStep( );
      page.clickNextStep( );
      page.clickNextStep( );
      page.affordLoanChoice( 'hourly' );
      page.clickNextStep( );
      page.clickNextStep( );
      page.clickNextStep( );
      page.actionPlan( 'consider' );
      page.clickNextStep( );
    } );
  } );
} );
