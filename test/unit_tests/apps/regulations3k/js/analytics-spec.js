import {
  getExpandable,
  getExpandableState,
  handleContentClick,
  handleNavClick,
  sendEvent,
} from '../../../../../cfgov/unprocessed/apps/regulations3k/js/analytics.js';

describe('The Regs3K analytics', () => {
  it('should send events', () => {
    const mockEvent = sendEvent('click', 'sidebar');

    expect(mockEvent).toEqual({
      event: 'eRegs Event',
      action: 'click',
      label: 'sidebar',
    });
  });

  it('should send events with custom categories', () => {
    const mockEvent = sendEvent('click', 'sidebar', 'eregs');

    expect(mockEvent).toEqual({
      event: 'eregs',
      action: 'click',
      label: 'sidebar',
    });
  });

  it('should find expandables', () => {
    const mockTarget = {
      classList: {
        contains: () => true,
      },
    };
    const event = {
      target: {
        closest: () => mockTarget,
      },
    };
    const expandable = getExpandable(event);

    expect(expandable).toEqual(mockTarget);
  });

  it('should get expandable state', () => {
    const mockEl = {
      classList: {
        contains: () => true,
      },
    };
    const mockEl2 = {
      classList: {
        contains: () => false,
      },
    };
    const state1 = getExpandableState(mockEl);
    expect(state1).toEqual('open');
    const state2 = getExpandableState(mockEl2);
    expect(state2).toEqual('close');
  });

  it('should handle navigation clicks on regs links', () => {
    let event = {
      target: {
        href: '/policy-compliance/rulemaking/regulations/1002/11/',
      },
    };
    event = handleNavClick(event);

    expect(event).toEqual({
      action: 'toc:click',
      event: 'eRegs Event',
      label: '1002-11',
    });
  });

  it('should handle navigation clicks on interp links', () => {
    let mockEvent = {
      target: {
        href: '/policy-compliance/rulemaking/regulations/1002/Interp-2/',
      },
    };
    mockEvent = handleNavClick(mockEvent);

    expect(mockEvent).toEqual({
      action: 'toc:click',
      event: 'eRegs Event',
      label: '1002-Interp-2',
    });
  });

  it('should handle navigation clicks on non-regs links', () => {
    let mockEvent = {
      target: {
        href: 'https://example.com',
      },
    };
    mockEvent = handleNavClick(mockEvent);

    expect(mockEvent).toBeUndefined();
  });

  it('should handle navigation clicks on non-links', () => {
    let mockEvent = { target: {} };
    mockEvent = handleNavClick(mockEvent);

    expect(mockEvent).toBeUndefined();
  });

  it('should handle content clicks on expandables', () => {
    let mockEvent = {
      target: {
        classList: {
          contains: () => true,
        },
        closest: () => null,
        getAttribute: () => 'Section 1',
      },
    };
    mockEvent = handleContentClick(mockEvent);

    expect(mockEvent).toEqual({
      action: 'interpexpandables:open',
      event: 'eRegs Event',
      label: 'Section 1',
    });
  });

  it('should handle content clicks on non-expandables', () => {
    let mockEvent = {
      target: {
        classList: {
          contains: () => false,
        },
        closest: () => null,
        getAttribute: () => 'Section 1',
      },
    };
    mockEvent = handleContentClick(mockEvent);

    expect(mockEvent).toBeUndefined();
  });
});
