'use strict';

const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const domManipulators = require(
  BASE_JS_PATH + 'modules/util/dom-manipulators'
);

describe( 'Dom Manipulators create', () => {
  before( () => {
    this.jsdom = require( 'jsdom-global' )();
  } );

  after( () => this.jsdom() );

  before( () => {
    const heading = domManipulators.create( 'h1', {
      'textContent': 'Create Heading Text',
      'id':          'create-heading-id',
      'className':   'create-heading-class',
      'data-name':   'create-heading-data'
    } );

    domManipulators.create( 'span', {
      'textContent': 'Heading Span',
      'id':          'create-span-id',
      'className':   'create-span-class',
      'data-name':   'create-span-data',
      'inside':      heading
    } );

    document.body.appendChild( heading );

    domManipulators.create( 'div', {
      'id':        'create-div-id',
      'className': 'create-div-class',
      'data-name': 'create-div-data',
      'around':    heading
    } );
  } );


  it( 'should create a single elem', () => {
    const query = document.querySelector( 'h1' );

    expect( query.id ).to.equal( 'create-heading-id' );
    expect( query.className ).to.equal( 'create-heading-class' );
    expect( query.getAttribute( 'data-name' ) )
      .to.equal( 'create-heading-data' );
  } );

  it( 'should create an elem inside another', () => {
    const query = document.querySelector( 'span' );

    expect( query.textContent ).to.equal( 'Heading Span' );
    expect( query.id ).to.equal( 'create-span-id' );
    expect( query.className ).to.equal( 'create-span-class' );
    expect( query.getAttribute( 'data-name' ) )
      .to.equal( 'create-span-data' );
  } );

  it( 'should create an elem around another', () => {
    const query = document.querySelector( 'div' );

    expect( query.id ).to.equal( 'create-div-id' );
    expect( query.className ).to.equal( 'create-div-class' );
    expect( query.getAttribute( 'data-name' ) )
      .to.equal( 'create-div-data' );
  } );
} );
