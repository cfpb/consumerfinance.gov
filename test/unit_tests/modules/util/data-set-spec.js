'use strict';

const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const dataSet = require( BASE_JS_PATH + 'modules/util/data-set' ).dataSet;

const chai = require( 'chai' );
const expect = chai.expect;
const jsdom = require( 'mocha-jsdom' );
const sinon = require( 'sinon' );
let sandbox;
let baseDom;

const HTML_SNIPPET =
  '<div data-test-value-a="testValueA"' +
        'data-test-value-B="testValueB"' +
        'data-testValue-C="testValueC"' +
        'data-test-ValuE-D="testValueD"' +
        'data-TEST-value-E="testValueE" >' +
    'testValue' +
  '</div>';

// JSdom hasn't implmented Element.dataset so I used Chrome to determine
// the correct values : http://jsfiddle.net/0j9u66h0/13/.
const datasetLookup = {
  testValueA: 'testValueA',
  testValueB: 'testValueB',
  testvalueC: 'testValueC',
  testValueD: 'testValueD',
  testValueE: 'testValueE'
};

describe( 'data-set', () => {
  jsdom();

  beforeEach( () => {
    sandbox = sinon.sandbox.create();
    document.body.innerHTML = HTML_SNIPPET;
    baseDom = document.querySelector( 'div' );
  } );

  afterEach( () => {
    sandbox.restore();
  } );

  it( 'should have the correct keys and values when using utility', () => {
    const dataset = dataSet( baseDom );
    expect( JSON.stringify( dataset ) ===
      JSON.stringify( datasetLookup ) ).to.equal( true );
  } );
} );
