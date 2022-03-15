import { PfcFinancialPathToGraduation } from './financial-path-helpers';

const page = new PfcFinancialPathToGraduation();

describe( 'Your Financial Path to Graduation (url parameter functionality)', () => {
  before( () => {
    cy.visit( '/paying-for-college/your-financial-path-to-graduation/?iped=163286&pid=4502-3&houp=onCampus&typp=bachelors&prop=0&lenp=3&ratp=inState&depp=dependent&cobs=n&tuit=10595&hous=12809&diro=13&book=1250&indo=55&tran=44&pelg=11&seog=12&fedg=13&stag=14&schg=15&tuig=16&othg=17&mta=18&gi=19&othm=20&stas=21&schs=22&oths=23&wkst=33&subl=299&unsl=399&insl=599&insr=0.06&insf=0.02&stal=499&star=0.05&staf=0.01&npol=699&npor=0.07&npof=0.03&pers=81&fams=82&529p=83&offj=84&onj=85&eta=86&othf=87&houx=31&fdx=32&clhx=33&trnx=34&hltx=35&entx=36&retx=37&taxx=38&chcx=39&dbtx=40&othx=41' );
  } );

  it( 'should choose the correct school', () => {
    cy.get( '#search__school-input' ).should( 'have.value', 'University of Maryland-College Park' );
  } );

  it( 'should choose the correct program options', () => {
    cy.get( 'input[name="programType"]:checked' ).should( 'have.value', 'bachelors' );
    cy.get( 'input[name="programProgress"]:checked' ).should( 'have.value', '0' );
    cy.get( 'input[name="programLength"]:checked' ).should( 'have.value', '3' );
    cy.get( 'input[name="programHousing"]:checked' ).should( 'have.value', 'onCampus' );
    cy.get( 'input[name="programDependency"]:checked' ).should( 'have.value', 'dependent' );
  } );

  it( 'should choose the correct program', () => {
    cy.get( '#program-select option:checked' ).should( 'have.value', '4502-3' );
    cy.get( '#program-select option:checked' ).should( 'contain', 'Bachelor\'s degree - Anthropology' );
  } );

  it( 'should have the correct direct costs values', () => {
    page.clickNextStep( );
    cy.get( '#costs__tuition-fees' ).should( 'have.value', '$10,595' );
    cy.get( '#costs__room-board' ).should( 'have.value', '$12,809' );
    cy.get( '#costs__other-direct' ).should( 'have.value', '$13' );
  } );

  it( 'should have the correct indirect costs values', () => {
    cy.get( '#costs__books' ).should( 'have.value', '$1,250' );
    cy.get( '#costs__transportation' ).should( 'have.value', '$44' );
    cy.get( '#costs__other-indirect' ).should( 'have.value', '$55' );
  } );

  it( 'should have the correct grants & scholarships values', () => {
    page.clickNextStep( );
    cy.get( '#grants__pell' ).should( 'have.value', '$11' );
    cy.get( '#grants__seog' ).should( 'have.value', '$12' );
    cy.get( '#grants__otherFederal' ).should( 'have.value', '$13' );
    cy.get( '#grants__state' ).should( 'have.value', '$14' );
    cy.get( '#grants__school' ).should( 'have.value', '$15' );
    cy.get( '#grants__tuition' ).should( 'have.value', '$16' );
    cy.get( '#grants__other' ).should( 'have.value', '$17' );
    cy.get( '#grants__mta' ).should( 'have.value', '$18' );
    cy.get( '#grants__gibill' ).should( 'have.value', '$19' );
    cy.get( '#grants_serviceOther' ).should( 'have.value', '$20' );
    cy.get( '#scholarships__state' ).should( 'have.value', '$21' );
    cy.get( '#scholarships__school' ).should( 'have.value', '$22' );
    cy.get( '#scholarships__other' ).should( 'have.value', '$23' );
  } );

  it( 'should have the correct work study values', () => {
    page.clickNextStep( );
    cy.get( '#workStudy__workStudy' ).should( 'have.value', '$33' );
  } );

  it( 'should have the correct federal loan values', () => {
    page.clickNextStep( );
    cy.get( '#loans__directSub' ).should( 'have.value', '$299' );
    cy.get( '#loans__directUnsub' ).should( 'have.value', '$399' );
  } );

  it( 'should have the correct school/other loan values', () => {
    page.clickNextStep( );
    cy.get( '#loans__stateLoan' ).should( 'have.value', '$499' );
    cy.get( '#loans__stateLoanRate' ).should( 'have.value', '5.00%' );
    cy.get( '#loans__stateLoanFee' ).should( 'have.value', '1.000%' );
    cy.get( '#loans__schoolLoan' ).should( 'have.value', '$599' );
    cy.get( '#loans__schoolLoanRate' ).should( 'have.value', '6.00%' );
    cy.get( '#loans__schoolLoanFee' ).should( 'have.value', '2.000%' );
    cy.get( '#loans__nonprofitLoan' ).should( 'have.value', '$699' );
    cy.get( '#loans__nonprofitLoanRate' ).should( 'have.value', '7.00%' );
    cy.get( '#loans__nonprofitLoanFee' ).should( 'have.value', '3.000%' );
  } );

  it( 'should have the correct other sources values', () => {
    page.clickNextStep( );
    cy.get( '#savings__personal' ).should( 'have.value', '$81' );
    cy.get( '#savings__family' ).should( 'have.value', '$82' );
    cy.get( '#savings__collegeSavings' ).should( 'have.value', '$83' );
    cy.get( '#income__jobOffCampus' ).should( 'have.value', '$84' );
    cy.get( '#income__jobOnCampus' ).should( 'have.value', '$85' );
    cy.get( '#income__employerAssist' ).should( 'have.value', '$86' );
    cy.get( '#income_otherFunding' ).should( 'have.value', '$87' );
  } );

  it( 'should have the correct expenses values', () => {
    cy.get( '#expenses__housing' ).should( 'have.value', '$31' );
    cy.get( '#expenses__food' ).should( 'have.value', '$32' );
    cy.get( '#expenses__clothing' ).should( 'have.value', '$33' );
    cy.get( '#expenses__transportation' ).should( 'have.value', '$34' );
    cy.get( '#expenses__healthcare' ).should( 'have.value', '$35' );
    cy.get( '#expenses__entertainment' ).should( 'have.value', '$36' );
    cy.get( '#expenses__savings' ).should( 'have.value', '$37' );
    cy.get( '#expenses__taxes' ).should( 'have.value', '$38' );
    cy.get( '#expenses__childcare' ).should( 'have.value', '$39' );
    cy.get( '#expenses__currentDebts' ).should( 'have.value', '$40' );
    cy.get( '#expenses__other' ).should( 'have.value', '$41' );
  } );

} );
