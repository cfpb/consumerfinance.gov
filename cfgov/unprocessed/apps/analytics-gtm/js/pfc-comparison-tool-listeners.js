import $ from 'jquery';

// Paying for College custom analytics file

const PFCAnalytics = ( function() {
  // -- Delay calculations after keyup --//
  const delay = ( function() {
    let t = 0;
    return function( callback, delay ) {
      clearTimeout( t );
      t = setTimeout( callback, delay );
    };
  } )(); // end delay()

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
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'School Cost Comparison',
      label: 'School Removed'
    } );
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
        window.dataLayer.push( {
          event: 'School Interactions',
          action: 'Reached Zero Left to Pay',
          label: schoolID
        } );
      }
    }, 1000 );
  } );

  // Fire an event when a tooltip is clicked
  $( '.tooltip-info' ).click( function( event ) {
    const tooltip = $( this ).attr( 'data-tipname' );
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'Tooltip Clicked',
      label: tooltip
    } );
  } );

  // Fire an event when GI Bill panel opens
  $( ".gibill-calculator, input[data-nickname='gibill']" ).click( function() {
    const columnNumber = $( this ).parents( '[data-column]' ).attr( 'data-column' );
    const schoolID = $( "#institution-row [data-column='" + columnNumber + "']" ).attr( 'data-schoolid' );
    delay( function() {
      const GIPanel = $( '[data-column="' + columnNumber + '"] .gibill-panel' );
      if ( GIPanel.is( ':visible' ) ) {
        window.dataLayer.push( {
          event: 'School Interactions',
          action: 'GI Bill Calculator Opened',
          label: schoolID
        } );
      }
    }, 500 );
  } );

  // Fire various events for rate-change clicks
  $( '.rate-change' ).click( function() {
    const buttonID = $( this ).attr( 'data-buttonid' );
    if ( $.inArray( buttonID, rateChangeClicks ) === -1 ) {
      rateChangeClicks.push( buttonID );
      window.dataLayer.push( {
        event: 'School Interactions',
        action: 'Percent Arrow Clicked',
        label: buttonID
      } );
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

    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'GI Bill Calculator Submit',
      label: schoolID
    } );
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'Military Status',
      label: serving
    } );
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'Cumulative service',
      label: tier
    } );
    if ( control === 'Public' ) {
      window.dataLayer.push( {
        event: 'School Interactions',
        action: 'GI Residency',
        label: residency
      } );
    }
  } );

  // Fire an event when Send Email is clicked
  $( '#send-email' ).click( function() {
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'Save and Share',
      label: 'Send email'
    } );
  } );

  // Fire an event when save draw is opened
  $( '#save-and-share' ).click( function( event, nateeve ) {
    let UNDEFINED;
    if ( nateeve === UNDEFINED ) {
      window.dataLayer.push( {
        event: 'School Interactions',
        action: 'Save and Share',
        label: 'toggle button'
      } );
    }
  } );

  // Fire an event when save current is clicked
  $( '#save-current' ).click( function() {
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'Save and Share',
      label: 'Save current worksheet'
    } );
  } );

  $( '#unique' ).click( function() {
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'Save and Share',
      label: 'Copy URL'
    } );
  } );

  $( '#save-drawer .save-share-facebook' ).click( function() {
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'Save and Share',
      label: 'Facebook_saveshare'
    } );
  } );

  $( '#save-drawer .save-share-twitter' ).click( function() {
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'Save and Share',
      label: 'Twitter_saveshare'
    } );
  } );

  // Fire an event when Get Started is clicked
  $( '#get-started-button' ).click( function() {
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'School Cost Comparison',
      label: 'Get Started Button'
    } );
  } );

  // Fire an event when Add a School is cancelled
  $( '#introduction .add-cancel' ).click( function() {
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'School Cost Comparison',
      label: 'Cancel Button'
    } );
  } );

  // Fire an event when Continue is clicked
  $( '#introduction .continue' ).click( function() {
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'School Cost Comparison',
      label: 'Continue Button'
    } );
    console.log( '#introduction .continue clicked' );
  } );

  // Fire an event when Add another school is clicked
  $( '#introduction .add-another-school' ).click( function() {
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'School Cost Comparison',
      label: 'Add another school Button'
    } );
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
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'Total Schools Added',
      label: schoolCount
    } );
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'School Added',
      label: schoolID
    } );
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'Program Type',
      label: program
    } );
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'Program Length',
      label: prgmlength
    } );


    if ( offer === 'Yes' ) {
      window.dataLayer.push( {
        event: 'School Interactions',
        action: 'Financial Aid Clicked'
      } );
      if ( $( '#xml-text' ).val() === '' && kbyoss === 'Yes' ) {
        window.dataLayer.push( {
          event: 'School Interactions',
          action: 'School Added - XML',
          label: 'Blank'
        } );
      } else if ( $( '#xml-text' ).val() !== '' && kbyoss === 'Yes' ) {
        window.dataLayer.push( {
          event: 'School Interactions',
          action: 'School Added - XML',
          label: 'XML text'
        } );
      }
    } else {
      window.dataLayer.push( {
        event: 'School Interactions',
        action: 'Housing',
        label: housing
      } );
      if ( control === 'Public' ) {
        window.dataLayer.push( {
          event: 'School Interactions',
          action: 'Residency',
          label: residency
        } );
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
    window.dataLayer.push( {
      event: 'School Interactions',
      action: 'Drop Down',
      label: arrwName
    } );
  } );

} )( $ );
