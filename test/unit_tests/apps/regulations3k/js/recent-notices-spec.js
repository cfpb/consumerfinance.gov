import { enableFetchMocks } from 'jest-fetch-mock';
import { simulateEvent } from '../../../../util/simulate-event.js';
import {
  processNotice,
  processNotices,
} from '../../../../../cfgov/unprocessed/apps/regulations3k/js/recent-notices.js';

enableFetchMocks();

const HTML_SNIPPET = `
  <ul id="regs3k-notices"></ul>
`;

// Mock console logging
delete global.console;
global.console = { error: jest.fn(), log: jest.fn() };

describe('The Regs3K search page', () => {
  beforeEach(() => {
    // Load HTML fixture
    document.body.innerHTML = HTML_SNIPPET;
  });

  afterEach(() => {
    fetch.resetMocks();
  });

  it('should process a notice', () => {
    const notice = {
      // eslint-disable-next-line camelcase
      html_url: 'https://federalregister.gov/',
      title: 'Really great notice',
    };
    const processedNotice = processNotice(notice);
    expect(processedNotice.constructor.name).toEqual('HTMLLIElement');
    expect(processedNotice.className).toEqual('m-list_link');
    expect(processedNotice.querySelector('a').href).toEqual(
      'https://federalregister.gov/'
    );
  });

  it('should process notices', () => {
    /* eslint-disable camelcase */
    const notices = [
      {
        html_url: 'https://federalregister.gov/1',
        title: 'Really great notice',
      },
      {
        html_url: 'https://federalregister.gov/2',
        title: 'Another really great notice',
      },
    ];
    /* eslint-enable camelcase */
    const processedNotices = processNotices(notices);
    expect(processedNotices.querySelectorAll('li').length).toEqual(3);
    expect(processedNotices.querySelectorAll('a')[2].textContent).toContain(
      'More'
    );
  });

  it('should load recent notices', () => {
    // Fire `load` event
    simulateEvent('load', window, { currentTarget: window });

    // Wait for window.load to trigger.
    setTimeout(() => {
      const numNotices = document.querySelectorAll('.m-list_link').length;
      expect(numNotices).toEqual(4);
    }, 1000);
  });

  it('should fail to load recent notices', (done) => {
    fetch.mockReject(new Error('Server error!'));

    // Fire `load` event
    simulateEvent('load', window, { currentTarget: window });

    setTimeout(() => {
      // eslint-disable-next-line no-console
      expect(console.error).toBeCalled();
      done();
    }, 100);
  });
});
