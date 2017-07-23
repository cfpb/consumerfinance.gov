'use strict';

const BASE_OAH_JS_PATH = require( '../../config' ).BASE_OAH_JS_PATH;
const expect = require( 'chai' ).expect;
const jsdom = require( 'mocha-jsdom' );

describe( 'Humanize loan type', function() {

  let $;
  let humanize;

  jsdom();

  before( function() {
    $ = require( 'jquery' );
    humanize = require( BASE_OAH_JS_PATH + '/modules/humanize-loan-type.js' );
  } );

  it( 'should convert conf to conventional', function() {
    var loan = 'conf';
    loan = humanize( loan );
    expect( loan ).to.eql( 'conventional' );
  } );

  it( 'should capitalize other stuff', function() {
    var loan = 'foo';
    loan = humanize( loan );
    expect( loan ).to.eql( 'FOO' );
  } );

} );
