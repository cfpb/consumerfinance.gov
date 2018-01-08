/* eslint no-unused-vars: "off" */


const BASE_JS_PATH = '../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;

const HTML_SNIPPET = '';

describe( 'FilterableListControls', () => {
  before( () => {
    this.jsdom = require( 'jsdom-global' )( HTML_SNIPPET );
    const FilterableListControls =
      require( BASE_JS_PATH + 'organisms/FilterableListControls' );
  } );

  after( () => this.jsdom() );

  // TODO: Implement tests.
} );
