'use strict';
var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var sinon = require( 'sinon' );
var View = exports.View =  require( './../fixtures/View.js' );
var glob = require( 'glob' );

runTest();
testAllViews();

function testAllViews() {
  glob( './src/static/js/**/*View.js', '', function ( er, files ) {
    for ( var len = files.length, i = 0; i < len; i++ ) {
      View = exports.View = require( '../../../' + files[i] );
      if ( View ) {
        runTest();
      }
    }
  } );
}

function runTest() {

  describe( 'View', function() {
    var viewInstance;
    var viewInstancewithEl;

    jsdom();

    beforeEach( function() {
      viewInstance = new View();
      viewInstancewithEl = new View( { el: document.createElement( 'div' ) } );
    } );

    context( 'has a constructor and it', function() {
      it( 'should be passed an object', function() {
        var constructorSpy = sinon.spy( exports, 'View' );
        View = exports.View;
        new View( {} ); // eslint-disable-line max-statements, no-inline-comments, max-len
        var arg0 = constructorSpy.args && constructorSpy.args[0];
        expect( arg0 !== null && typeof arg0 === 'object' ).to.be.true;
      } );

      it( 'should set the el property', function() {
        expect( viewInstancewithEl.el ).to.exist;
      } );

      it( 'should set the el property to be a DOM element', function() {
        expect( viewInstancewithEl.el instanceof HTMLElement ).to.be.true;
      } );
    } );

    it( 'should have an initialize function', function() {
      expect( viewInstance.initialize ).to.exist;
      expect( typeof viewInstance.initialize === 'function' ).to.be.true;
    } );

    it( 'should have called the initialize function', function() {
      var initializeSpy = sinon.spy( View.prototype, 'initialize' );
      new View();
      expect( initializeSpy.called ).to.be.true;
    } );

    it( 'should have a render function', function() {
      expect( viewInstance.render ).to.exist;
      expect( typeof viewInstance.render === 'function' ).to.be.true;
    } );

    context( 'render function has been called and it', function() {
      it( 'should have set the el property', function() {
        viewInstance.render();
        expect( viewInstance.el ).to.exist;
      } );

      it( 'should have set the el property to be a DOM element', function() {
        viewInstance.render();
        expect( viewInstance.el instanceof HTMLElement ).to.be.true;
      } );

      it( 'should have set rendered property to be true', function() {
        viewInstance.render();
        expect( viewInstance.rendered ).to.be.true;
      } );
    } );

    it( 'should have a remove function', function() {
      expect( viewInstance.remove ).to.exist;
      expect( typeof viewInstance.remove === 'function' ).to.be.true;
    } );

    context( 'remove function has been called and it', function() {
      it( 'should have set the el property to be undefined', function() {
        viewInstance.remove();
        expect( viewInstance.el ).to.not.exist;
      } );

      it( 'should have removed the el element from the DOM', function() {
        var domEl;
        viewInstancewithEl.el.className = 'el';
        domEl = document.querySelector( '.el' );
        if ( domEl === null ) {
          document.body.appendChild( viewInstancewithEl.el );
        }
        viewInstancewithEl.remove();
        expect( document.querySelector( '.el' ) === null ).to.be.true;
      } );
    } );

  } );

}
