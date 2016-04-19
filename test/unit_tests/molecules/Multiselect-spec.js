'use strict';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var sinon = require( 'sinon' );

var BASE_JS_PATH = '../../../cfgov/unprocessed/js/';
var Multiselect = require( BASE_JS_PATH + 'molecules/Multiselect' );
var multiselect;
var selectDom;
var multiselectDom;
var HTML_SNIPPET =
    '<select name="test-select" id="test-select" multiple>' +
      '<option value="Debt collection">Debt collection</option>' +
      '<option value="Nonbanks">Nonbanks</option>' +
      '<option value="Mortgage disclosure">Mortgage disclosure</option>' +
      '<optgroup label="All other topics">' +
    '</select>';

describe( 'Multiselect', function() {
  jsdom();

  beforeEach( function() {
    document.body.innerHTML = HTML_SNIPPET

    selectDom = document.querySelector( 'select[multiple]' );
    multiselect =
      new Multiselect( selectDom );
  } );

  describe( 'init', function() {
    it( 'should intitialize the Multiselect', function() {
      multiselect.init();
      selectDom = document.querySelectorAll( 'select[multiple]' );
      multiselectDom = document.querySelectorAll( '.cf-multi-select' );

      expect( selectDom.length ).to.equal( 0 );
      expect( multiselectDom.length ).to.equal( 1 );
    } );
  } );

  describe( 'dom creation', function() {
    xit( 'should autocheck any selected options (form submitted pages)', function() {
      var options = selectDom.querySelectorAll( 'option' );
      options[0].selected = 'selected';
      multiselect.init();
      var choices = document.querySelectorAll( '.cf-multi-select_choices li' );

      expect( choices.length ).to.equal( 1 );
    } );
  } );
} );
