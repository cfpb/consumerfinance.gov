import { init as tabInit } from '../../../../../../cfgov/unprocessed/apps/owning-a-home/js/explore-rates/tab.js';
import { simulateEvent } from '../../../../../util/simulate-event.js';

const HTML_SNIPPET = `
  <section class="next-steps tabs-layout">
    <ul class="tabs">
      <li class="tab-list active-tab">
          <a class="tab-link" href="#tab1">Tab 1</a>
      </li>
      <li class="tab-list">
          <a class="tab-link" href="#tab2">Tab 2</a>
      </li>
    </ul>

    <div id="tab1" class="tab-content default">
      Tab 1 content.
    </div>
    <div id="tab2" class="tab-content">
      Tab 2 content.
    </div>
  </section>
`;

let tabLink2;
let tabContentDom1;
let tabContentDom2;

describe('explore-rates/params', () => {
  beforeEach(() => {
    document.body.innerHTML = HTML_SNIPPET;
    tabLink2 = document.querySelectorAll('.tab-link')[1];
    tabContentDom1 = document.querySelector('#tab1');
    tabContentDom2 = document.querySelector('#tab2');
  });

  it('should not have u-hidden before JS is initialized.', () => {
    expect(tabContentDom1.classList.contains('u-hidden')).toBe(false);
    expect(tabContentDom2.classList.contains('u-hidden')).toBe(false);
  });

  it('should add u-hidden class when JS is initialized.', () => {
    tabInit();
    expect(tabContentDom1.classList.contains('u-hidden')).toBe(false);
    expect(tabContentDom2.classList.contains('u-hidden')).toBe(true);
  });

  it('should move u-hidden class when tab is clicked.', () => {
    tabInit();
    simulateEvent('click', tabLink2);
    expect(tabContentDom1.classList.contains('u-hidden')).toBe(true);
    expect(tabContentDom2.classList.contains('u-hidden')).toBe(false);
  });
});
