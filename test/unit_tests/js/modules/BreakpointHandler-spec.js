const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
let BreakpointHandler;
let args;

/**
 * Change the viewport to width x height. Mocks window.resizeTo( w, h ).
 * @param  {number} width - width in pixels.
 * @param  {number} height - height in pixels.
 */
function windowResizeTo( width, height ) {
  // Change the viewport to width x height. Mocks window.resizeTo( w, h ).
  global.innerWidth = width;
  global.innerHeight = height;

  // Trigger the window resize event.
  global.dispatchEvent( new Event( 'resize' ) );
}

describe( 'BreakpointHandler', () => {
  beforeEach( () => {
    args = {
      enter:      jest.fn(),
      leave:      jest.fn(),
      breakpoint: 600
    };

    BreakpointHandler = require( BASE_JS_PATH + 'modules/BreakpointHandler' );
  } );

  it( 'should throw an error if passed incomplete arguments', () => {
    const errorTxt = 'BreakpointHandler constructor requires arguments!';
    function createBreakpointInstance() {
      return new BreakpointHandler();
    }

    expect( createBreakpointInstance ).toThrow( errorTxt );
  } );

  it( 'should correctly create BreakpointHandler instances', () => {
    const breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.watchWindowResize ).toBeInstanceOf( Function );
    expect( breakpointHandler.handleViewportChange ).toBeInstanceOf( Function );
    expect( breakpointHandler.testBreakpoint ).toBeInstanceOf( Function );

    expect( breakpointHandler.match ).toBe( false );
    expect( breakpointHandler.type === 'max' ).toBe( true );
  } );

  it( 'should allow responsive breakpoints as arguments', () => {
    args.breakpoint = 'bpXS';
    let breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.breakpoint ).toStrictEqual( 600 );
    expect( breakpointHandler.type === 'max' ).toBe( true );
    expect( breakpointHandler.testBreakpoint( 300 ) ).toBe( true );

    args.breakpoint = 'bpSM';
    args.type = 'min';
    breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.breakpoint ).toStrictEqual( 601 );
    expect( breakpointHandler.type === 'min' ).toBe( true );
    expect( breakpointHandler.testBreakpoint( 601 ) ).toBe( true );
  } );

  it( 'should test a breakpoint', () => {
    let breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.testBreakpoint( 601 ) ).toBe( false );

    args.type = 'min';
    breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.testBreakpoint( 601 ) ).toBe( true );

    args.type = 'range';
    args.breakpoint = [ 0, 600 ];
    breakpointHandler = new BreakpointHandler( args );
    expect( breakpointHandler.testBreakpoint( 300 ) ).toBe( true );
    expect( breakpointHandler.testBreakpoint( 601 ) ).toBe( false );
  } );

  it( 'should handle viewport changes', () => {
    let breakpointHandler = new BreakpointHandler( args );
    let enterSpy = jest.spyOn( breakpointHandler, 'enter' );
    let leaveSpy = jest.spyOn( breakpointHandler, 'leave' );
    const mockDate = {
      isBpLG: false,
      isBpMED: false,
      isBpSM: false,
      isBpXL: false,
      isBpXS: false
    };

    windowResizeTo( 598, 800 );
    expect( enterSpy ).toHaveBeenCalled();
    mockDate.isBpXS = true;
    expect( enterSpy ).toHaveBeenCalledWith( mockDate );
    mockDate.isBpXS = false;

    windowResizeTo( 601, 800 );
    expect( leaveSpy ).toHaveBeenCalled();
    mockDate.isBpSM = true;
    expect( leaveSpy ).toHaveBeenCalledWith( mockDate );
    mockDate.isBpSM = false;

    args.type = 'min';
    args.breakpoint = 901;
    breakpointHandler = new BreakpointHandler( args );
    enterSpy = jest.spyOn( breakpointHandler, 'enter' );
    windowResizeTo( 1000, 800 );
    expect( enterSpy ).toHaveBeenCalled();
    mockDate.isBpMED = true;
    expect( enterSpy ).toHaveBeenCalledWith( mockDate );
    mockDate.isBpMED = false;

    args.type = 'max';
    args.breakpoint = 1020;
    breakpointHandler = new BreakpointHandler( args );
    leaveSpy = jest.spyOn( breakpointHandler, 'leave' );
    windowResizeTo( 1021, 800 );
    expect( leaveSpy ).toHaveBeenCalled();
    mockDate.isBpLG = true;
    expect( leaveSpy ).toHaveBeenCalledWith( mockDate );
    mockDate.isBpLG = false;
  } );

  it( 'should watch for window resize events', () => {
    const breakpointHandler = new BreakpointHandler( args );
    const handleViewportChangeSpy = jest.spyOn(
      breakpointHandler, 'handleViewportChange'
    );

    expect( handleViewportChangeSpy ).toHaveBeenCalledTimes( 0 );
    windowResizeTo( 1200, 800 );
    expect( handleViewportChangeSpy ).toHaveBeenCalledTimes( 1 );
  } );
} );
