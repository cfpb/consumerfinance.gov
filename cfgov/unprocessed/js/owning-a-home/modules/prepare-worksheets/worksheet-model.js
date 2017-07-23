'use strict';

var _config = require( './worksheet-config' );
var _uuid = require( './util/uuid' );
var $ = require( 'jquery' );

var _dataStore = {
  worksheets: {}
};

// CRUD operations for the worksheet as a whole.
this.setWorksheet = function( type, value ) {
  _dataStore.worksheets[type] = value;
};

this.getWorksheet = function( type ) {
  return _dataStore.worksheets[type];
};

this.deleteWorksheet = function( type ) {
  delete _dataStore.worksheets[type];
};

this.resetWorksheet = function( type ) {
  var worksheet = this.getDefaultWorksheet( type );
  this.setDefaultWorksheet( type, worksheet );
  return worksheet;
};

this.getDefaultWorksheet = function( type ) {
  return _config.worksheetDefaults[type]();
};

this.setDefaultWorksheet = function( type, worksheet ) {
  // Add ids to rows.
  worksheet = worksheet || [];
  var row;
  for ( var i = 0; i < worksheet.length; i++ ) {
    row = worksheet[i];
    row.uid = _uuid.generateIdentifier();
  }
  // Add blank input row.
  worksheet.push( _getDefaultRow() );
  // Set this worksheet on dataStore.
  this.setWorksheet( type, worksheet );

  return worksheet;
};

this.getDefaultData = function() {
  return _config.getAllWorksheetDefaults();
};

this.setDefaultData = function() {
  var worksheet;
  var data = this.getDefaultData();

  for ( worksheet in data ) {
    if ( data.hasOwnProperty( worksheet ) ) {
      this.setDefaultWorksheet( worksheet, data[worksheet] );
    }
  }
};

// CRUD operations for the worksheet rows.
this.deleteWorksheetRow = function( type, rowID ) {
  // TODO -- check that this row is deletable
  var worksheet = _dataStore.worksheets[type];
  var idx = findRowById( worksheet, rowID );
  if ( !isNaN( parseInt( idx, 10 ) ) ) {
    worksheet.splice( idx, 1 );
  }
};

this.getWorksheetRow = function( type, row ) {
  row = _dataStore.worksheets[type][row];
  if ( !row ) {
    throw new Error( 'Requested row out of worksheet bounds!' );
  }
  return row;
};

this.addWorksheetRow = function( type, opts ) {
  var row = _getDefaultRow();
  if ( opts ) {
    $.extend( row, opts );
  }
  row.uid = _uuid.generateIdentifier();
  _dataStore.worksheets[type].push( row );
  return row;
};

this.setWorksheetRow = function( type, row, data ) {
  for ( var key in data ) {
    if ( data.hasOwnProperty( key ) ) {
      this.setWorksheetProperty( type, row, key, data[key] );
    }
  }
};

// CRUD operations for the worksheet properties.
this.setWorksheetProperty = function( type, row, key, value ) {
  row[key] = value;
};

this.getWorksheetProperty = function( type, row, key ) {
  return this.getWorksheet( type )[row][key];
};

this.deleteWorksheetProperty = function( type, row, key ) {
  var value = '';
  if ( key === 'grade' ) {
    value = null;
  }
  this.setWorksheetProperty( type, row, key, value );
};

// Utility methods.
this.setData = function( data ) {
  _dataStore = data;
};

this.getData = function() {
  return _dataStore;
};

function findRowById( worksheetRows, rowID ) {
  var idx;
  for ( var i = 0; i < worksheetRows.length; i++ ) {
    if ( worksheetRows[i].uid === rowID ) {
      idx = i;
    }
  }
  return idx;
}

// Data manipulation.

this.combineGoals = function() {
  // TODO: when financial goals are added:
  return this.getWorksheet( 'personal' ).concat( this.getWorksheet( 'financial' ) ) || [];
};

this.filterEmptyRows = function( worksheet, opts ) {
  // Filters out worksheet rows without text values
  // opts.requireGrade = true will also filter out items without grades
  // opts.skipLast = true will allow blank values for last item
  // TODO: add delete option?
  var filteredWorksheet = [];
  var len = worksheet.length - 1;
  var i = 0;
  var item;
  opts = opts || {};

  function isEmpty( item, lastItem ) {
    if ( lastItem && opts.skipLast ) { return false; }
    if ( !item.text ) { return true; }
    if ( opts.requireGrade && ( !item.grade && item.grade !== 0 ) ) {
      return true;
    }

    return false;
  }

  for ( i; i <= len; i++ ) {
    item = worksheet[i];
    if ( !isEmpty( item, i === len ) ) {
      filteredWorksheet.push( item );
    }
  }

  return filteredWorksheet;
};

this.sortWorksheetByGrade = function( worksheet, type ) {
  var sorted = [];
  var labels = _config.gradeSummaryLabels[type];
  var lenLabels = labels.length;
  var lenWorksheet = worksheet.length;
  var i = 0;
  var l = 0;

  // Add an item to the 'sorted' array for each of the grade labels.
  for ( l; l < lenLabels; l++ ) {
    sorted[l] = { title: labels[l], items: [], type: type };
  }

  // Add each graded worksheet row to the appropriate grade bucket.
  for ( i; i < lenWorksheet; i++ ) {
    var item = worksheet[i];
    var grade = item.grade;
    // if there's an object for this grade, add this item to its items array
    ( ( sorted[grade] || {} ).items || [] ).push( item );
  }

  return sorted;
};

// Private methods.
function _getDefaultRow() {
  return _config.getWorksheetRowDefaults();
}
