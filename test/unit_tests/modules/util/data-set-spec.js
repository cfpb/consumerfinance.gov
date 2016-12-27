'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
var dataSet = require( BASE_JS_PATH + 'modules/util/data-set' ).dataSet;

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var sinon = require( 'sinon' );
var sandbox;
var baseDom;

var HTML_SNIPPET =
  '<div data-test-value-a="testValueA"' +
        'data-test-value-B="testValueB"' +
        'data-testValue-C="testValueC"' +
        'data-test-ValuE-D="testValueD"' +
        'data-TEST-value-E="testValueE" >' +
    'testValue' +
  '</div>';

// JSdom hasn't implmented Element.dataset so I used Chrome to determine
// the correct values : http://jsfiddle.net/0j9u66h0/13/.
var datasetLookup = {
  testValueA: 'testValueA',
  testValueB: 'testValueB',
  testvalueC: 'testValueC',
  testValueD: 'testValueD',
  testValueE: 'testValueE'
};

describe( 'data-set', function() {
  jsdom();

  beforeEach( function() {
    sandbox = sinon.sandbox.create();
    document.body.innerHTML = HTML_SNIPPET;
    baseDom = document.querySelector( 'div' );
  } );

  afterEach( function() {
    sandbox.restore();
  } );

  it( 'should have the correct keys and values when using utility',
    function() {
      var dataset = dataSet( baseDom );
      expect( JSON.stringify( dataset ) ===
        JSON.stringify( datasetLookup ) ).to.equal( true );
    }
  );
} );
