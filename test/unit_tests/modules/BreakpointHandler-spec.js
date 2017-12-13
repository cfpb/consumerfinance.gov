const chai = require( 'chai' );
const expect = chai.expect;
const sinon = require( 'sinon' );
let BreakpointHandler;
let args;
const BASE_LOC = '../../../cfgov/unprocessed/js/';
const standardType = require( BASE_LOC + 'modules/util/standard-type' );

describe( 'BreakpointHandler', () => {
  before( () => {
    this.jsdom = require( 'jsdom-global' )( '', {
      beforeParse( win ) {
        const resizeEvent = win.document.createEvent( 'Event' );
        resizeEvent.initEvent( 'resize', true, true );

        win.resizeTo = function( width, height ) {
          this.innerWidth = this.outerWidth = width;
          this.innerHeight = this.outerHeight = height;
          win.dispatchEvent( resizeEvent );
        };

        win.useMock = function() {
          const mockwin = {
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

    // Simulate window resize event
    const resizeEvent = document.createEvent( 'Event' );
    resizeEvent.initEvent( 'resize', true, true );

    global.window.resizeTo = ( width, height ) => {
      global.window.innerWidth = width || global.window.innerWidth;
      global.window.innerHeight = height || global.window.innerHeight;
      global.window.dispatchEvent( resizeEvent );
    };
  } );

  after( () => this.jsdom() );

  beforeEach( () => {
    args = {
      enter:      standardType.noopFunct,
      leave:      standardType.noopFunct,
      breakpoint: 600
    };

    BreakpointHandler = require( BASE_LOC + 'modules/BreakpointHandler' );
  } );

  it( 'should throw an error if passed incomplete arguments', () => {
    const errorTxt = 'BreakpointHandler constructor requires arguments!';
    function createBreakpointInstance() {
      return new BreakpointHandler();
    }

    expect( createBreakpointInstance ).to.throw( errorTxt );
  } );

  it( 'should compute window width properly on older browsers', () => {
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

  it( 'should correctly create BreakpointHandler instances', () => {
    const breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.watchWindowResize )
      .to.be.an.instanceof( Function );
    expect( breakpointHandler.handleViewportChange )
      .to.be.an.instanceof( Function );
    expect( breakpointHandler.testBreakpoint )
      .to.be.an.instanceof( Function );

    expect( breakpointHandler.match ).to.be.false;
    expect( breakpointHandler.type === 'max' ).to.be.true;
  } );

  it( 'should allow responsive breakpoints as arguments', () => {
    args.breakpoint = 'bpXS';
    let breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.breakpoint ).to.equal( 600 );
    expect( breakpointHandler.type === 'max' ).to.be.true;
    expect( breakpointHandler.testBreakpoint( 300 ) ).to.be.true;

    args.breakpoint = 'bpSM';
    args.type = 'min';
    breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.breakpoint ).to.equal( 601 );
    expect( breakpointHandler.type === 'min' ).to.be.true;
    expect( breakpointHandler.testBreakpoint( 601 ) ).to.be.true;
  } );

  it( 'should test a breakpoint', () => {
    let breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.testBreakpoint( 601 ) ).to.be.false;

    args.type = 'min';
    breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.testBreakpoint( 601 ) ).to.be.true;

    args.type = 'range';
    args.breakpoint = [ 0, 600 ];
    breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.testBreakpoint( 300 ) ).to.be.true;
    expect( breakpointHandler.testBreakpoint( 601 ) ).to.be.false;
  } );

  it( 'should handle viewport changes', () => {
    let breakpointHandler = new BreakpointHandler( args );
    let enterSpy = sinon.spy( breakpointHandler, 'enter' );
    let leaveSpy = sinon.spy( breakpointHandler, 'leave' );

    window.resizeTo( 598, 800 );
    expect( enterSpy.calledOnce ).to.be.true;
    expect( enterSpy.calledWithMatch( sinon.match.has( 'isBpXS', true ) ) )
      .to.be.true;

    window.resizeTo( 601, 800 );
    expect( leaveSpy.calledOnce ).to.be.true;
    expect( leaveSpy.calledWithMatch( sinon.match.has( 'isBpSM', true ) ) )
      .to.be.true;

    args.type = 'min';
    args.breakpoint = 901;
    breakpointHandler = new BreakpointHandler( args );
    enterSpy = sinon.spy( breakpointHandler, 'enter' );
    window.resizeTo( 1000, 800 );
    expect( enterSpy.calledOnce ).to.be.true;
    expect( enterSpy.calledWithMatch( sinon.match.has( 'isBpMED', true ) ) )
      .to.be.true;

    args.type = 'max';
    args.breakpoint = 1020;
    breakpointHandler = new BreakpointHandler( args );
    leaveSpy = sinon.spy( breakpointHandler, 'leave' );
    window.resizeTo( 1021, 800 );
    expect( leaveSpy.calledOnce ).to.be.true;
    expect( leaveSpy.calledWithMatch( sinon.match.has( 'isBpLG', true ) ) )
      .to.be.true;
  } );

  it( 'should watch for window resize events', () => {
    const breakpointHandler = new BreakpointHandler( args );
    const handleViewportChangeSpy =
    sinon.spy( breakpointHandler, 'handleViewportChange' );

    expect( handleViewportChangeSpy.called ).to.be.false;
    window.resizeTo( 1200, 800 );
    expect( handleViewportChangeSpy.called ).to.be.true;
  } );

} );
