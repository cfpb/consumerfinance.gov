'use strict';

var monthly = {};

monthly.preTaxIncomeTotal = function( data ) {
  return parseFloat( data.preTaxIncome || 0 ) +
         parseFloat( data.preTaxIncomeCB || 0 );
};

monthly.takeHomeIncomeTotal = function( data ) {
  return parseFloat( data.takeHomeIncome || 0 ) +
         parseFloat( data.takeHomeIncomeCB || 0 );
};

monthly.spendingAndSavings = function( data ) {
  var sum = parseFloat( data.rent || 0 ) +
            parseFloat( data.utilities || 0 ) +
            parseFloat( data.debtPayments || 0 ) +
            parseFloat( data.livingExpenses || 0 ) +
            parseFloat( data.savings || 0 );

  return sum;
};

monthly.homeMaintenanceAndImprovement = function( data ) {
  return parseFloat( data.homeImprovement || 0 ) +
         parseFloat( data.homeMaintenance || 0 );
};

monthly.newHomeownershipExpenses = function( data ) {
  return parseFloat( data.condoHOA || 0 ) +
         monthly.homeMaintenanceAndImprovement( data );
};

monthly.futureSavings = function( data ) {
  return parseFloat( data.emergencySavings || 0 ) +
         parseFloat( data.longTermSavings || 0 );
};

monthly.availableHousingFunds = function( data ) {
  var income = monthly.takeHomeIncomeTotal( data );
  var expenses = parseFloat( data.debtPayments || 0 ) +
                 parseFloat( data.livingExpenses || 0 ) +
                 parseFloat( data.futureUtilities || 0 ) +
                 monthly.futureSavings( data || 0 ) +
                 monthly.homeMaintenanceAndImprovement( data || 0 );

  return income - expenses;
};

monthly.estimatedTotalPayment = function( data ) {
  return monthly.availableHousingFunds( data ) - parseFloat( data.condoHOA || 0 );
};

monthly.taxesAndInsurance = function( data ) {
  var homePrice = parseFloat( data.homePrice || 0 );
  var propertyTax = parseFloat( ( data.propertyTax || 0 ) / 100 );
  var insurance = parseFloat( data.homeownersInsurance || 0 );
  var annualTaxesAndInsurance = homePrice * propertyTax + insurance;
  return annualTaxesAndInsurance / 12;
};

monthly.principalAndInterest = function( data ) {
  var total = monthly.estimatedTotalPayment( data ) - monthly.taxesAndInsurance( data );
  return total;
};

monthly.percentageIncomeAvailable = function( data ) {
  var funds = monthly.availableHousingFunds( data );
  var income = monthly.preTaxIncomeTotal( data );
  if ( income ) {
    return Math.round( funds / income * 100 );
  }

  return NaN;
};

module.exports = monthly;
