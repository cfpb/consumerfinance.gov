'use strict';

const BASE_JS_PATH = '../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const jsdom = require( 'mocha-jsdom' );

describe( 'FilterableListControls', () => {
  jsdom();

  before( () => {
    const FilterableListControls =
     require( BASE_JS_PATH + 'organisms/FilterableListControls' );
  } );

  // TODO: Implement tests.
} );
