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
var sandbox;
var HTML_SNIPPET =
    '<select name="test-select" id="test-select" multiple>' +
      '<option value="Debt collection">Debt collection</option>' +
      '<option value="consumers-responses">Consumer&#39;s Responses</option>' +
      '<option value="Mortgage disclosure">Mortgage disclosure</option>' +
      '<optgroup label="All other topics">' +
    '</select>';

function keyPress( target, key ) {
  var event = target.createEvent( 'Event' );
  event.keyCode = key;
  event.initEvent( 'keydown' );
  target.dispatchEvent( event );
}

describe( 'Multiselect', function() {

  jsdom();

  beforeEach( function() {
    sandbox = sinon.sandbox.create();

    document.body.innerHTML = HTML_SNIPPET;

    selectDom = document.querySelector( 'select[multiple]' );
    multiselect = new Multiselect( selectDom );
  } );

  afterEach( function() {
    sandbox.restore();
  } );

  describe( 'init', function() {
    it( 'should intitialize the Multiselect', function() {
      multiselect.init();
      selectDom = document.querySelectorAll( 'select[multiple]' );
      multiselectDom = document.querySelectorAll( '.cf-multi-select' );

      expect( selectDom.length ).to.equal( 0 );
      expect( multiselectDom.length ).to.equal( 1 );
    } );

    it( 'should autocheck any selected options (form submitted pages)',
      function() {
        var option = document.querySelector( 'option' );
        option.defaultSelected = true;
        multiselect.init();
        var choices =
          document.querySelectorAll( '.cf-multi-select_choices li' );

        expect( choices.length ).to.equal( 1 );
        expect( choices[0].innerHTML ).to.contain( 'Debt collection' );
      }
    );

    it( 'should log a helpful tip if passed a bad option value', function() {
      // TODO: Remove console.log in favor of throwing an error.
      //       sandbox.stub console.log will prevent regular `console.log(…)`
      //       calls in this suite.
      sandbox.stub( window.console, 'log' );
      var option = document.querySelector( 'option' );
      option.value = 'Foo\'';
      multiselect.init();
      selectDom = document.querySelectorAll( 'select[multiple]' );
      multiselectDom = document.querySelectorAll( '.cf-multi-select' );

      expect( selectDom.length ).to.equal( 1 );
      expect( multiselectDom.length ).to.equal( 0 );
      sinon.assert.calledOnce( console.log );
      sinon.assert.calledWithExactly(
        console.log, '\'Foo\'\' is not a valid value'
      );
    } );
  } );

  describe( 'public methods', function() {
    it( 'should open when the expand method is called', function() {
      multiselect.init();
      multiselect.expand();
      multiselectDom = document.querySelector( '.cf-multi-select' );
      var fieldset =
        multiselectDom.querySelector( '.cf-multi-select_fieldset' );

      expect( multiselectDom.className ).to.equal( 'cf-multi-select active' );
      expect( fieldset.getAttribute( 'aria-hidden' ) ).to.equal( 'false' );
    } );

    it( 'should close when the collapse method is called', function() {
      multiselect.init();
      multiselect.expand();
      multiselect.collapse();
      multiselectDom = document.querySelector( '.cf-multi-select' );
      var fieldset =
        multiselectDom.querySelector( '.cf-multi-select_fieldset' );

      expect( multiselectDom.className ).to.equal( 'cf-multi-select' );
      expect( fieldset.getAttribute( 'aria-hidden' ) ).to.equal( 'true' );
    } );
  } );

  describe( 'interactions', function() {
    xit( 'should open when the search input is clicked', function() {
      multiselect.init();
      multiselectDom = document.querySelector( '.cf-multi-select' );
      var fieldset =
        multiselectDom.querySelector( '.cf-multi-select_fieldset' );
      var search = document.querySelector( '#test-select' );
      search.click();

      expect( document.activeElement.id ).to.equal( 'test-select' );
      expect( multiselectDom.className ).to.equal( 'cf-multi-select active' );
      expect( fieldset.getAttribute( 'aria-hidden' ) ).to.equal( 'false' );
    } );

    xit( 'should highlight the first item when keying down', function() {
      multiselect.init();
      var search = document.querySelector( '#test-select' );
      search.click();
      keyPress( search, 40 );

      expect( document.activeElement.id ).to.equal( 'Debt collection' );
    } );

    xit( 'should close when the body is clicked', function() {
      multiselect.init();
      multiselect.expand();
      multiselectDom = document.querySelector( '.cf-multi-select' );
      var fieldset =
        multiselectDom.querySelector( '.cf-multi-select_fieldset' );
      document.click();

      expect( multiselectDom.className ).to.equal( 'cf-multi-select' );
      expect( fieldset.getAttribute( 'aria-hidden' ) ).to.equal( 'true' );
    } );
  } );
} );
