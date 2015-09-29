'use strict';
var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var ariaState =
require( '../../../../cfgov/v1/preprocessed/js/modules/util/aria-state.js' );
var element;
var obj;

describe( 'ARIA state', function() {

  jsdom();

  beforeEach( function() {
    obj = { isTest: true };
    element = document.createElement( 'div' );
    document.body.appendChild( element );
  } );

  it( 'should create a state object with the correct ARIA state', function() {
    var state = ariaState.create( 'expanded', element );
    expect( state.isExpanded ).to.be.false;
    expect( element.getAttribute( 'aria-expanded' ) === 'false' ).to.be.true;

    state = ariaState.create( 'disabled', element );
    expect( state.isDisabled ).to.be.false;
    expect( element.getAttribute( 'aria-disabled' ) === 'false' ).to.be.true;
  } );

  it( 'should throw errors when created with invalid arguments', function() {
    var errorTxt = 'Invalid Arguments';
    expect( ariaState.create.bind( 'expanded', '' ) ).to.throw( errorTxt );
    expect( ariaState.create.bind( 'closed', element ) ).to.throw( errorTxt );
  } );

  it( 'should define the correct ARIA state property and attribute',
    function() {
      ariaState.define( 'invalid', element, obj );
      expect( obj.hasOwnProperty( 'isInvalid' ) ).to.be.true;
      expect( element.getAttribute( 'aria-invalid' ) === 'false' ).to.be.true;

      this.isGrabbed = true;
      ariaState.define( 'grabbed', element, this );
      expect( this.hasOwnProperty( 'isGrabbed' ) ).to.be.true;
      expect( element.getAttribute( 'aria-grabbed' ) === 'true' ).to.be.true;
      delete this.isGrabbed;
    } );

  it( 'should change the ARIA state after state property changes', function() {
    var state = ariaState.create( 'hidden', element );
    expect( element.getAttribute( 'aria-hidden' ) === 'false' ).to.be.true;
    state.isHidden = true;
    expect( element.getAttribute( 'aria-hidden' ) === 'true' ).to.be.true;

    ariaState.define( 'selected', element, obj );
    expect( element.getAttribute( 'aria-selected' ) === 'false' ).to.be.true;
    obj.isSelected = true;
    expect( element.getAttribute( 'aria-selected' ) === 'true' ).to.be.true;
  } );

} );
