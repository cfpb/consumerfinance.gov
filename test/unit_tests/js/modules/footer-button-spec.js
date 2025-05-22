import { jest } from '@jest/globals';
import { init as FooterButtonInit } from '../../../../cfgov/unprocessed/js/modules/footer-button.js';
import { simulateEvent } from '../../../util/simulate-event.js';

let footerBtnDom;

const HTML_SNIPPET = `
<div class="skip-nav">
    <a class="a-btn skip-nav__link" href="#main">
        Skip to main content
    </a>
</div>

<a class="a-btn
                          a-btn--secondary
                          a-btn--full-on-xs
                          u-mb45"
   data-gtm_ignore="true"
   data-js-hook="behavior_return-to-top"
   data-cy="btn-back-to-top"
   href="#">
    Back to top
</a>
`;

/**
 * Mock window.scrollTo() method.
 * @param {number} xCoord - An x coordinate.
 * @param {number} yCoord - A y coordinate.
 */
function scrollTo(xCoord, yCoord) {
  window.scrollX = xCoord;
  window.scrollY = yCoord;
}

describe('footer-button', () => {
  beforeAll(() => {
    window.scrollTo = scrollTo;
    document.body.innerHTML = HTML_SNIPPET;
    footerBtnDom = document.querySelector('[data-cy=btn-back-to-top]');
  });

  it(
    'button should scroll when clicked ' +
      'and requestAnimationFrame is supported',
    (done) => {
      window.scrollY = 10;
      FooterButtonInit();
      simulateEvent('click', footerBtnDom);

      window.setTimeout(() => {
        expect(window.scrollY).toBe(0);
        done();
      }, 2000);
    },
  );

  it(
    'button should scroll when clicked ' +
      'and requestAnimationFrame is not supported',
    () => {
      jest.spyOn(window, 'scrollTo');
      delete window.requestAnimationFrame;
      window.scrollY = 10;
      FooterButtonInit();
      simulateEvent('click', footerBtnDom);

      expect(window.scrollTo).toHaveBeenCalledWith(0, 0);
    },
  );
});
