'use strict';
var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var sinon = require( 'sinon' );
var BreakpointHandler;
var args;
var BASE_LOC = '../../../../cfgov/preprocessed/js/';


beforeEach( function() {
  args = {
    enter:      function() {},
    leave:      function() {},
    breakpoint: 599
  };

  BreakpointHandler = require( BASE_LOC + 'modules/classes/BreakpointHandler' );
} );

describe( 'BreakpointHandler', function() {

  jsdom( {
    created: function( error, win ) {
      if ( error ) {
        console.log( error ); // eslint-disable-line no-console, no-inline-comments, max-len
      }

      var resizeEvent = win.document.createEvent( 'Event' );
      resizeEvent.initEvent( 'resize', true, true );

      win.resizeTo = function( width, height ) {
        this.innerWidth = this.outerWidth = width;
        this.innerHeight = this.outerHeight = height;
        win.dispatchEvent( resizeEvent );
      };

      win.useMock = function() {
        var mockwin = {
          addEventListener: win.addEventListener,
          document:         { documentElement: {}},
          innerWidth:       win.innerWidth,
          innerHeight:      win.innerHeight,
          resizeTo:         win.resizeTo
        };

        mockwin.document.documentElement.clientWidth =
        win.document.documentElement.clientWidth;

        mockwin.document.body = win.document.body;

        mockwin.restore = function() {
          global.window = win;
          global.document = win.document;
        };

        global.window = mockwin;
        global.document = mockwin.document;
      };
    }
  } );

  it( 'should throw an error if passed incomplete arguments', function() {
    var errorTxt = 'BreakpointHandler constructor requires arguments!';
    function createBreakpointInstance() {
      return new BreakpointHandler();
    }

    expect( createBreakpointInstance ).to.throw( errorTxt );
  } );

  it( 'should compute window width properly on older browsers', function() {
    function createBreakpointInstance() {
      return new BreakpointHandler( args );
    }

    window.useMock();
    delete window.innerWidth;
    expect( createBreakpointInstance ).to.not.throw( Error );

    delete window.document.documentElement;
    expect( createBreakpointInstance ).to.not.throw( Error );
    window.restore();
  } );

  it( 'should correctly create BreakpointHandler instances', function() {
    var breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.watchWindowResize )
    .to.be.an.instanceof( Function );
    expect( breakpointHandler.handleViewportChange )
    .to.be.an.instanceof( Function );
    expect( breakpointHandler.testBreakpoint )
    .to.be.an.instanceof( Function );

    expect( breakpointHandler.match ).to.be.false;
    expect( breakpointHandler.type === 'max' ).to.be.true;
  } );

  it( 'should allow responsive breakpoints as arguments', function() {
    args.breakpoint = 'mobile';
    var breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.breakpoint ).to.equal( 599 );
    expect( breakpointHandler.type === 'max' ).to.be.true;
    expect( breakpointHandler.testBreakpoint( 300 ) ).to.be.true;

    args.breakpoint = 'tablet';
    args.type = 'min';
    breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.breakpoint ).to.equal( 600 );
    expect( breakpointHandler.type === 'min' ).to.be.true;
    expect( breakpointHandler.testBreakpoint( 601 ) ).to.be.true;
  } );

  it( 'should test a breakpoint', function() {
    var breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.testBreakpoint( 600 ) ).to.be.false;

    args.type = 'min';
    breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.testBreakpoint( 600 ) ).to.be.true;

    args.type = 'range';
    args.breakpoint = [ 0, 599 ];
    breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.testBreakpoint( 300 ) ).to.be.true;
    expect( breakpointHandler.testBreakpoint( 600 ) ).to.be.false;
  } );

  it( 'should handle viewport changes', function() {
    var breakpointHandler = new BreakpointHandler( args );
    var enterSpy = sinon.spy( breakpointHandler, 'enter' );
    var leaveSpy = sinon.spy( breakpointHandler, 'leave' );

    window.resizeTo( 598, 800 );
    expect( enterSpy.calledOnce ).to.be.true;
    expect( enterSpy.calledWithMatch( sinon.match.has( 'isMobile', true ) ) )
    .to.be.true;

    window.resizeTo( 601, 800 );
    expect( leaveSpy.calledOnce ).to.be.true;
    expect( leaveSpy.calledWithMatch( sinon.match.has( 'isTablet', true ) ) )
    .to.be.true;

    args.type = 'min';
    args.breakpoint = 801;
    breakpointHandler = new BreakpointHandler( args );
    enterSpy = sinon.spy( breakpointHandler, 'enter' );
    window.resizeTo( 1199, 800 );
    expect( enterSpy.calledOnce ).to.be.true;
    expect( enterSpy.calledWithMatch( sinon.match.has( 'isDesktop', true ) ) )
    .to.be.true;

    args.type = 'max';
    args.breakpoint = 1199;
    breakpointHandler = new BreakpointHandler( args );
    leaveSpy = sinon.spy( breakpointHandler, 'leave' );
    window.resizeTo( 1200, 800 );
    expect( leaveSpy.calledOnce ).to.be.true;
    expect( leaveSpy.calledWithMatch( sinon.match.has( 'isWall', true ) ) )
    .to.be.true;
  } );

  it( 'should watch for window resize events', function() {
    var breakpointHandler = new BreakpointHandler( args );
    var handleViewportChangeSpy =
    sinon.spy( breakpointHandler, 'handleViewportChange' );

    expect( handleViewportChangeSpy.called ).to.be.false;
    window.resizeTo( 1200, 800 );
    expect( handleViewportChangeSpy.called ).to.be.true;
  } );

} );
