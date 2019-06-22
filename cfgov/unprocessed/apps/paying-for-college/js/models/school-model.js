// TODO: Remove jquery.
const $ = require( 'jquery' );

const schoolModel = {
  values: {},

  init: function( nationalData, schoolData, programData ) {

    $.extend( this.values, schoolData, programData, nationalData );

    // Initialize default rate
    this.values.programDefaultRate = programData.defaultRate;
    this.values.schoolDefaultRate = schoolData.defaultRate;
    this.values.programCompletionRate = programData.completionRate;
    this.values.schoolCompletionRate = schoolData.completionRate;
    this.values.defaultRateSource = 'program';
    if ( programData.defaultRate === 'None' ) {
      this.values.defaultRate = schoolData.defaultRate;
      this.values.defaultRateSource = 'school';
    }

    // Process values from the API
    this.values = this.processBLSExpenses( this.values );
    this.gradRate = 'null';
    return this.processAPIData( this.values );
  },

  /**
   * Fixes certain API values for use in this app
   * @param {object} values - object containing unformatted API values
   * @returns {object} object with reformatted values
   */
  processAPIData: function( values ) {
    values.settlementSchool = Boolean( values.settlementSchool );
    values.jobRate = values.jobRate || '';
    values.programLength /= 12;
    if ( values.programSalary === null ) {
      if ( values.schoolSalary === null ) {
        values.medianSalary = values.nationalSalary;
        values.salarySource = 'national';
      } else {
        values.medianSalary = values.schoolSalary;
        values.salarySource = 'school';
      }
    } else {
      values.medianSalary = values.programSalary;
      values.salarySource = 'program';
    }
    values.monthlySalary = Math.round( Number( values.medianSalary ) / 12 );
    values.medianSchoolDebt = values.medianStudentLoanCompleters ||
      values.medianTotalDebt;
    if ( values.hasOwnProperty( 'completionRate' ) &&
      values.completionRate !== 'None' ) {
      values.gradRate = values.completionRate;
      values.gradRateSource = 'program';
    } else {
      values.gradRateSource = 'school';
    }

    return values;
  },

  processBLSExpenses: function( values ) {
    /* BLS expense data is delivered as annual values.
       The tool displays monthly expenses. */

    if ( values.region === 'Not available' ) {
      values.BLSAverage = 'national';
      values.monthlyRent = Math.round( values.nationalHousing / 12 );
      values.monthlyFood = Math.round( values.nationalFood / 12 );
      values.monthlyTransportation =
        Math.round( values.nationalTransportation / 12 );
      values.monthlyInsurance = Math.round( values.nationalHealthcare / 12 );
      values.monthlySavings = Math.round( values.nationalRetirement / 12 );
      values.monthlyOther =
        Math.round( values.nationalEntertainment / 12 );
    } else {
      values.BLSAverage = values.region + ' regional';
      values.monthlyRent = Math.round( values.regionalHousing / 12 );
      values.monthlyFood = Math.round( values.regionalFood / 12 );
      values.monthlyTransportation =
        Math.round( values.regionalTransportation / 12 );
      values.monthlyInsurance = Math.round( values.regionalHealthcare / 12 );
      values.monthlySavings = Math.round( values.regionalRetirement / 12 );
      values.monthlyOther =
        Math.round( values.regionalEntertainment / 12 );
    }
    return values;
  }


};
module.exports = schoolModel;
