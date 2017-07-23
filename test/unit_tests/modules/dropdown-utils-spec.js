'use strict';

const BASE_OAH_JS_PATH = require( '../../config' ).BASE_OAH_JS_PATH;
const expect = require( 'chai' ).expect;
const jsdom = require( 'mocha-jsdom' );
let dropDown;
let $;
let dd;

describe( 'Dropdown utils', function() {

  jsdom();

  before( function() {
    $ = require( 'jquery' );
    dropDown = require( BASE_OAH_JS_PATH + '/modules/dropdown-utils.js' );
  } );

  beforeEach( function() {
    $( 'body' ).html( $( '<div class="foo"><select id="foo"><option value="baz"></option></select></div>' ) );
  } );

  it( 'should complain if you don\'t specify a target', function() {
    expect( dropDown ).to.throw();
  } );

  it( 'should disable dropdowns', function() {
    dropDown( 'foo' ).disable();
    expect( $( '#foo' ).attr( 'disabled' ) ).to.equal( 'disabled' );
  } );

  it( 'should enable dropdowns', function() {
    dropDown( 'foo' ).disable();
    dropDown( 'foo' ).enable();
    expect( $( '#foo' ).attr( 'disabled' ) ).to.be.undefined;
  } );

  it( 'should add options to dropdowns', function() {
    dropDown( 'foo' ).addOption( { label: 'foo', value: 'bar' } );
    dropDown( 'foo' ).addOption( { label: 'foo1', value: 'bar1' } );
    dropDown( 'foo' ).addOption( { label: 'foo2', value: 'bar2' } );
    expect( $( 'option' ) ).to.have.length( 4 );
  } );

  it( 'should not add options with same values', function() {
    dropDown( 'foo' ).addOption( { label: 'first', value: 'bar' } );
    dropDown( 'foo' ).addOption( { label: 'second', value: 'bar' } );
    expect( $( 'option' ) ).to.have.length( 2 );
  } );

  it( 'should select the option when values.select is true', function() {
    dropDown( 'foo' ).addOption( { label: 'Foo', value: 'BAR', select: 1 } );
    expect( $( '#foo' )[0].selectedIndex ).to.equal( 1 );
  } );

  it( 'should create option with value/name of ""', function() {
    dropDown( 'foo' ).addOption( null );
    $( '#foo' )[0].selectedIndex = 1;
    expect( $( '#foo' ).val() ).to.equal( '' );
  } );

  it( 'should disable all given options', function() {
    dropDown( 'foo' ).addOption( { value: 'value1', label: 'label1' } );
    dropDown( 'foo' ).addOption( { value: 'value2', label: 'label2' } );
    expect( $( 'option:disabled' ) ).to.have.length( 0 );
    dropDown( 'foo' ).disable( [ 'value1', 'value2' ] );
    expect( $( 'option:disabled' ).length ).to.equal( 2 );
  } );

  it( 'should select several select elements', function() {
    $( 'body' ).append( '<select id="foo1"><option value="baz1"></option></select>' );
    $( 'body' ).append( '<select id="foo2"><option value="baz1"></option></select>' );
    dropDown( [ 'foo', 'foo2' ] ).disable();
    expect( $( 'select :disabled' ) ).to.have.length( 2 );
    dropDown( [ 'foo', 'foo1', 'foo2' ] ).enable();
    expect( $( 'select :enabled' ) ).to.have.length( 3 );
    expect( $( 'select :disabled' ) ).to.have.length( 0 );
  } );

  it( 'should let methods be chainable', function() {
    dropDown( 'foo' ).addOption( { label: 'foo', value: 'bar' } ).addOption( { label: 'foo1', value: 'bar1' } ).addOption( { label: 'foo2', value: 'bar2' } );
    expect( $( 'option' ) ).to.have.length( 4 );
  } );

  it( 'should remove options from dropdowns', function() {
    dropDown( 'foo' ).addOption( { label: 'foo', value: 'bar' } );
    dropDown( 'foo' ).addOption( { label: 'foo1', value: 'bar1' } );
    dropDown( 'foo' ).removeOption( 'bar1' );
    expect( $( 'option' ) ).to.have.length( 2 );
  } );

  it( 'should complain if you try to remove an option without specifying a value', function() {
    expect( dropDown( 'foo' ).removeOption ).to.throw();
  } );

  it( 'should complain if you try to check an option without specifying a value', function() {
    expect( dropDown( 'foo' ).hasOption ).to.throw();
  } );

  it( 'should report if a dropdown has an option', function() {
    dropDown( 'foo' ).addOption( { label: 'foo', value: 'bar' } );
    expect( dropDown( 'foo' ).hasOption( 'bar' ) ).to.be.true;
  } );

  it( 'should reset a dropdown', function() {
    dropDown( 'foo' ).addOption( { label: 'foo', value: 'bar' } );
    $( '#foo' )[0].selectedIndex = 1;
    dropDown( 'foo' ).reset();
    expect( $( '#foo' )[0].selectedIndex ).to.equal( 0 );
  } );

  it( 'should hide a dropdown', function() {
    dropDown( 'foo' ).hide();
    expect( $( '.foo' ).hasClass( 'hidden' ) ).to.be.true;
  } );

  it( 'should show a dropdown', function() {
    dropDown( 'foo' ).hide();
    dropDown( 'foo' ).show();
    expect( $( '.foo' ).hasClass( 'hidden' ) ).to.equal( false );
  } );

  it( 'should show loading', function() {
    dropDown( 'foo' ).showLoadingAnimation();
    expect( $( '.foo' ).hasClass( 'loading' ) ).to.equal( true );
  } );

  it( 'should hide loading', function() {
    dropDown( 'foo' ).showLoadingAnimation();
    dropDown( 'foo' ).hideLoadingAnimation();
    expect( $( '.foo' ).hasClass( 'loading' ) ).to.be.false;
  } );

  it( 'should highlight the dropdown', function() {
    dropDown( 'foo' ).showHighlight();
    expect( $( '.foo' ).hasClass( 'highlight-dropdown' ) ).to.be.true;
  } );

  it( 'should unhighlight the dropdown', function() {
    dropDown( 'foo' ).showHighlight();
    dropDown( 'foo' ).hideHighlight();
    expect( $( '.foo' ).hasClass( 'highlight-dropdown' ) ).to.be.false;
  } );

} );
