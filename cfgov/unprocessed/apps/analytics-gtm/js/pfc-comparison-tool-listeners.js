// TODO: Remove jquery.
import $ from 'jquery';

import {
  analyticsLog,
  delay,
  track
} from './util/analytics-util';

// Paying for College custom analytics file

const PFCAnalytics = ( function() {

  // -- findEmptyColumn() - finds the first empty column, returns column number [1-3] --//
  function findEmptyColumn() {
    let column = false;
    for ( let x = 1; x <= 3; x++ ) {
      const school_id = $( "#institution-row [data-column='" + x + "']" ).attr( 'data-schoolid' );
      if ( school_id === '' ) {
        column = x;
        break;
      }
    }
    return column;
  } // end findEmptyColumn()

  const global = {
    schoolsAdded: 0, emptyColumn: 1
  };
  const rateChangeClicks = [];
  const schoolsZeroed = [ 'example' ];

  // Fire an event when a school is removed.
  $( '.remove-confirm .remove-yes' ).click( function() {
    const columnNumber = $( this ).parents( '[data-column]' ).attr( 'data-column' );
    const schoolID = $( '#institution-row [data-column="' + columnNumber + '"]' ).attr( 'data-schoolid' );
    track( 'School Interactions', 'School Cost Comparison', 'School Removed' );
    // Important to add a School tracking - reset the global.emptyColumn var
    global.emptyColumn = findEmptyColumn();
  } );

  // Fire an event when Left to Pay = $0 and Costs > $0
  $( '#comparison-tables' ).on( 'keyup', 'input.school-data', function( ev ) {
    const columnNumber = $( this ).parents( '[data-column]' ).attr( 'data-column' );
    delay( function() {
      const totalCosts = $( '.breakdown [data-column="' + columnNumber + '"] .costs-value' ).html();
      const leftToPay = $( '.breakdown [data-column="' + columnNumber + '"] [data-nickname="gap"]' ).html();
      const schoolID = $( '#institution-row [data-column="' + columnNumber + '"]' ).attr( 'data-schoolid' );
      if ( leftToPay === '$0' && totalCosts !== '$0' ) {
        track( 'School Interactions', 'Reached Zero Left to Pay', schoolID );
      }
    }, 1000 );
  } );

  // Fire an event when a tooltip is clicked
  $( '.tooltip-info' ).click( function( event ) {
    const tooltip = $( this ).attr( 'data-tipname' );
    track( 'School Interactions', 'Tooltip Clicked', tooltip );
  } );

  // Fire an event when GI Bill panel opens
  $( ".gibill-calculator, input[data-nickname='gibill']" ).click( function() {
    const columnNumber = $( this ).parents( '[data-column]' ).attr( 'data-column' );
    const schoolID = $( "#institution-row [data-column='" + columnNumber + "']" ).attr( 'data-schoolid' );
    delay( function() {
      const GIPanel = $( '[data-column="' + columnNumber + '"] .gibill-panel' );
      if ( GIPanel.is( ':visible' ) ) {
        track( 'School Interactions', 'GI Bill Calculator Opened', schoolID );
      }
    }, 500 );
  } );

  // Fire various events for rate-change clicks
  $( '.rate-change' ).click( function() {
    const buttonID = $( this ).attr( 'data-buttonid' );
    if ( $.inArray( buttonID, rateChangeClicks ) === -1 ) {
      rateChangeClicks.push( buttonID );
      track( 'School Interactions', 'Percent Arrow Clicked', buttonID );
    }

  } );

  // Fire an event when clicking "Calculate" button
  $( '.gibill-panel .military-calculate' ).click( function() {
    const columnNumber = $( this ).closest( '[data-column]' ).attr( 'data-column' );
    const schoolID = $( "#institution-row [data-column='" + columnNumber + "']" ).attr( 'data-schoolid' );
    const serving = $( '[data-column="1"] .military-status-select :selected' ).html();
    const tier = $( "[data-column='1'] .military-tier-select" ).find( ':selected' ).html();
    const residency = $( "[data-column='1'] .military-residency-panel :radio:checked" ).val();
    const control = $( '.header-cell[data-column="' + columnNumber + '"]' ).attr( 'data-control' );

    track( 'School Interactions', 'GI Bill Calculator Submit', schoolID );
    track( 'School Interactions', 'Military Status', serving );
    track( 'School Interactions', 'Cumulative service', tier );
    if ( control === 'Public' ) {
      track( 'School Interactions', 'GI Residency', residency );
    }
  } );

  // Fire an event when Send Email is clicked
  $( '#send-email' ).click( function() {
    track( 'School Interactions', 'Save and Share', 'Send email' );
  } );

  // Fire an event when save draw is opened
  $( '#save-and-share' ).click( function( event, nateeve ) {
    let UNDEFINED;
    if ( nateeve === UNDEFINED ) {
      track( 'School Interactions', 'Save and Share', 'toggle button' );
    }
  } );

  // Fire an event when save current is clicked
  $( '#save-current' ).click( function() {
    track( 'School Interactions', 'Save and Share', 'Save current worksheet' );
  } );

  $( '#unique' ).click( function() {
    track( 'School Interactions', 'Save and Share', 'Copy URL' );
  } );

  $( '#save-drawer .save-share-facebook' ).click( function() {
    track( 'School Interactions', 'Save and Share', 'Facebook_saveshare' );
  } );

  $( '#save-drawer .save-share-twitter' ).click( function() {
    track( 'School Interactions', 'Save and Share', 'Twitter_saveshare' );
  } );

  // Fire an event when Get Started is clicked
  $( '#get-started-button' ).click( function() {
    track(
      'School Interactions', 'School Cost Comparison', 'Get Started Button'
    );
  } );

  // Fire an event when Add a School is cancelled
  $( '#introduction .add-cancel' ).click( function() {
    track( 'School Interactions', 'School Cost Comparison', 'Cancel Button' );
  } );

  // Fire an event when Continue is clicked
  $( '#introduction .continue' ).click( function() {
    track( 'School Interactions', 'School Cost Comparison', 'Continue Button' );
    analyticsLog( '#introduction .continue clicked' );
  } );

  // Fire an event when Add another school is clicked
  $( '#introduction .add-another-school' ).click( function() {
    track(
      'School Interactions',
      'School Cost Comparison',
      'Add another school Button'
    );
  } );

  // Fire an event when adding a school.
  function newSchoolEvent() {
    const schoolID = $( '#school-name-search' ).attr( 'data-schoolid' );
    const program = $( '#step-two input:radio[name="program"]:checked' ).val();
    const kbyoss = $( '#school-name-search' ).attr( 'data-kbyoss' );
    const prgmlength = String( $( '#step-two select[name="prgmlength"]' ).val() );
    const housing = $( 'input[name="step-three-housing"]:checked' ).val();
    const control = $( '#school-name-search' ).attr( 'data-control' );
    const residency = $( 'input[name="step-three-residency"]:checked' ).val();
    let offer = 'No';

    global.schoolsAdded++;
    const schoolCount = String( global.schoolsAdded );
    if ( $( '#finaidoffer' ).is( ':checked' ) ) {
      offer = 'Yes';
    }
    track( 'School Interactions', 'Total Schools Added', schoolCount );
    track( 'School Interactions', 'School Added', schoolID );
    track( 'School Interactions', 'Program Type', program );
    track( 'School Interactions', 'Program Length', prgmlength );

    if ( offer === 'Yes' ) {
      // TODO: Determine what the label should be for this?
      window.dataLayer.push( {
        event: 'School Interactions',
        action: 'Financial Aid Clicked'
      } );
      if ( $( '#xml-text' ).val() === '' && kbyoss === 'Yes' ) {
        track( 'School Interactions', 'School Added - XML', 'Blank' );
      } else if ( $( '#xml-text' ).val() !== '' && kbyoss === 'Yes' ) {
        track( 'School Interactions', 'School Added - XML', 'XML text' );
      }
    } else {
      track( 'School Interactions', 'Housing', housing );
      if ( control === 'Public' ) {
        track( 'School Interactions', 'Residency', residency );
      }
    }
  }

  // Check for a new school added when .continue and .add-another-school are clicked
  $( '#introduction .continue, #introduction .add-another-school' ).click( function() {
    delay( function() {
      const newEmpty = findEmptyColumn();
      if ( newEmpty !== global.emptyColumn ) {
        newSchoolEvent();
        global.emptyColumn = newEmpty;
      }
    }, 500 );

  } );

  // Fire event when user clicks the arrows to open sections
  $( '.arrw-collapse' ).click( function() {
    const arrwName = $( this ).attr( 'data-arrwname' );
    track( 'School Interactions', 'Drop Down', arrwName );
  } );

} )( $ );
