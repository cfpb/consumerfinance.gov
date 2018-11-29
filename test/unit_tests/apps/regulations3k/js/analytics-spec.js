import * as analytics from '../../../../../cfgov/unprocessed/apps/regulations3k/js/analytics.js';

/* eslint-disable max-lines-per-function, no-undefined */
describe( 'The Regs3K analytics', () => {

  it( 'should send events', () => {
    const mockEvent = analytics.sendEvent( 'click', 'sidebar' );

    expect( mockEvent ).toEqual( {
      event: 'eRegs Event',
      action: 'click',
      label: 'sidebar',
      eventCallback: undefined,
      eventTimeout: 500
    } );
  } );

  it( 'should send events with custom categories', () => {
    const mockEvent = analytics.sendEvent( 'click', 'sidebar', 'eregs' );

    expect( mockEvent ).toEqual( {
      event: 'eregs',
      action: 'click',
      label: 'sidebar',
      eventCallback: undefined,
      eventTimeout: 500
    } );
  } );

  it( 'should find expandables', () => {
    const mockTarget = {
      classList: {
        contains: () => true
      },
      parentNode: {
        matches: () => false
      }
    };
    const event = {
      target: mockTarget
    };
    const expandable = analytics.getExpandable( event );

    expect( expandable ).toEqual( mockTarget );
  } );

  it( 'should get expandable state', () => {
    const mockEl = {
      classList: {
        contains: () => true
      }
    };
    const mockEl2 = {
      classList: {
        contains: () => false
      }
    };
    const state1 = analytics.getExpandableState( mockEl );
    expect( state1 ).toEqual( 'open' );
    const state2 = analytics.getExpandableState( mockEl2 );
    expect( state2 ).toEqual( 'close' );
  } );

  it( 'should handle navigation clicks on regs links', () => {
    let event = { target: {
      href: '/policy-compliance/rulemaking/regulations/1002/11/'
    }};
    event = analytics.handleNavClick( event );

    expect( event ).toEqual( {
      action: 'toc:click',
      event: 'eRegs Event',
      eventCallback: undefined,
      eventTimeout: 500,
      label: '1002-11'
    } );
  } );

  it( 'should handle navigation clicks on interp links', () => {
    let mockEvent = { target: {
      href: '/policy-compliance/rulemaking/regulations/1002/Interp-2/'
    }};
    mockEvent = analytics.handleNavClick( mockEvent );

    expect( mockEvent ).toEqual( {
      action: 'toc:click',
      event: 'eRegs Event',
      eventCallback: undefined,
      eventTimeout: 500,
      label: '1002-Interp-2'
    } );
  } );

  it( 'should handle navigation clicks on non-regs links', () => {
    let mockEvent = { target: {
      href: 'https://example.com'
    }};
    mockEvent = analytics.handleNavClick( mockEvent );

    expect( mockEvent ).toBeUndefined();
  } );

  it( 'should handle navigation clicks on non-links', () => {
    let mockEvent = { target: {}};
    mockEvent = analytics.handleNavClick( mockEvent );

    expect( mockEvent ).toBeUndefined();
  } );

  it( 'should handle content clicks on expandables', () => {
    let mockEvent = {
      target: {
        classList: {
          contains: () => true
        },
        parentNode: {
          matches: () => false
        },
        getAttribute: () => 'Section 1'
      }
    };
    mockEvent = analytics.handleContentClick( mockEvent );

    expect( mockEvent ).toEqual( {
      action: 'interpexpandables:open',
      event: 'eRegs Event',
      eventCallback: undefined,
      eventTimeout: 500,
      label: 'Section 1'
    } );
  } );

  it( 'should handle content clicks on non-expandables', () => {
    let mockEvent = {
      target: {
        classList: {
          contains: () => false
        },
        parentNode: {
          matches: () => false
        },
        getAttribute: () => 'Section 1'
      }
    };
    mockEvent = analytics.handleContentClick( mockEvent );

    expect( mockEvent ).toBeUndefined();
  } );

} );
