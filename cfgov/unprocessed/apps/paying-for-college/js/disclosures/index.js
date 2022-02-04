// TODO: Remove jquery.
const $ = require( 'jquery' );

const fetch = require( './dispatchers/get-api-values' );
const verifyOffer = require( './dispatchers/post-verify' );
const financialModel = require( './models/financial-model' );
const schoolModel = require( './models/school-model' );
const expensesModel = require( './models/expenses-model' );
const getFinancial = require( './dispatchers/get-financial-values' );
const getExpenses = require( './dispatchers/get-expenses-values' );
const getUrlValues = require( './dispatchers/get-url-values' );
const financialView = require( './views/financial-view' );
const expensesView = require( './views/expenses-view' );
const metricView = require( './views/metric-view' );
const questionView = require( './views/question-view' );
const publish = require( './dispatchers/publish-update' );

require( './utils/print-page' );

const app = {
  init: function() {
  // jquery promise to delay full model creation until ajax resolves
    $.when( fetch.initialData() )
      .done( function( constants, expenses ) {
        financialModel.init( constants[0] );
        financialView.init();
        if ( location.href.indexOf( 'about-this-tool' ) === -1 ) {
          expensesModel.init( expenses[0] );
          expensesView.init();
        }
        if ( getUrlValues.urlOfferExists() ) {
          // Check for URL offer data
          const urlValues = getUrlValues.urlValues();
          $.when( fetch.schoolData( urlValues.collegeID, urlValues.programID ) )
            .done( function( schoolData, programData, nationalData ) {
              const data = {};
              $.extend( data, schoolData[0], programData[0], nationalData[0] );
              const schoolValues = schoolModel.init( nationalData[0], schoolData[0], programData[0] );

              /* If PID exists, update the financial model and view based
                 on program data */
              if ( !data.hasOwnProperty( 'pidNotFound' ) ) {
                financialModel.updateModelWithProgram( schoolValues );
                financialView.updateViewWithProgram( schoolValues, urlValues );
              }

              // Add url values to the financial model
              publish.extendFinancialData( urlValues );
              if ( typeof urlValues.totalCost === 'undefined' ) {
                publish.financialData( 'totalCost', null );
              }
              financialView.updateViewWithURL( schoolValues, urlValues );
              // initialize metric view
              metricView.init();
              financialView.updateView( getFinancial.values() );
              questionView.init();

              // Update expenses model bases on region and salary
              const region = schoolValues.BLSAverage.substr( 0, 2 );
              $( '#bls-region-select' ).val( region ).change();
            } );
        }
        // set financial caps based on data
        financialView.setCaps( getFinancial.values() );
        financialView.updateView( getFinancial.values() );
      } );
    verifyOffer.init();
  }
};

$( document ).ready( function() {
  app.init();

  /* The following line allows for functional testing by exposing
     the getFinancial method.
     $( '#financial-offer' ).data( 'getFinancial', getFinancial );
     console.log( $( '#financial-offer' ).data() ); */
  window.getFinancial = getFinancial;
  window.getExpenses = getExpenses;
} );
