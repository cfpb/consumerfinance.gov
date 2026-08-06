import HTML_SNIPPET from '../../mocks/megaMenuSnippet.js';
import { MegaMenu } from '../../../../cfgov/unprocessed/js/organisms/MegaMenu.js';
import { simulateEvent } from '../../../util/simulate-event.js';

describe('MegaMenuMobile', () => {
  let navElem;
  let megaMenu;

  beforeEach(() => {
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 420,
    });

    document.body.innerHTML = HTML_SNIPPET;
    navElem = document.querySelector('.o-mega-menu');
    megaMenu = new MegaMenu(navElem);
    megaMenu.init();
  });

  describe('sub-menu click handler', () => {
    it('should expand on the first level sub-menu button click', (done) => {
      const menuTrigger = navElem.querySelector('.o-mega-menu__trigger');
      const subTrigger = navElem.querySelector(
        '.o-mega-menu__content-1-link--has-children',
      );
      const firstPanel = navElem.querySelector('.o-mega-menu__content-1');
      const secondPanel = navElem.querySelector('.o-mega-menu__content-2');
      let isExpanded;

      /**
       * Resolve first click.
       */
      function resolveFirstClick() {
        simulateEvent('click', subTrigger);
        isExpanded = firstPanel.getAttribute('data-open');
        setTimeout(() => {
          expect(isExpanded).toEqual('true');
          done();
        }, 200);

        window.setTimeout(resolveSecondClick, 200);
      }

      /**
       * Resolve second click.
       */
      function resolveSecondClick() {
        isExpanded = secondPanel.getAttribute('data-open');
        expect(isExpanded).toEqual('true');
        done();
      }

      simulateEvent('click', menuTrigger);

      window.setTimeout(resolveFirstClick, 200);
    });

    it('should not be expanded by default', () => {
      const secondPanel = navElem.querySelector('.o-mega-menu__content-2');
      const isExpanded = secondPanel.getAttribute('data-open');

      expect(isExpanded).toEqual('false');
    });

    it('should not be expanded on the main trigger click', (done) => {
      const menuTrigger = navElem.querySelector('.o-mega-menu__trigger');
      const secondPanel = navElem.querySelector('.o-mega-menu__content-2');
      let isExpanded;

      /**
       * Resolve first click.
       */
      function resolveFirstClick() {
        isExpanded = secondPanel.getAttribute('data-open');

        expect(isExpanded).toEqual('false');
        done();
      }

      simulateEvent('click', menuTrigger);

      window.setTimeout(resolveFirstClick, 200);
    });

    it('should collapse on the first level sub-menu back button click', (done) => {
      const menuTrigger = navElem.querySelector('.o-mega-menu__trigger');
      const subTrigger = navElem.querySelector(
        '.o-mega-menu__content-1-link--has-children',
      );
      const secondPanel = navElem.querySelector('.o-mega-menu__content-2');
      const subAltTrigger = secondPanel.querySelector(
        '.o-mega-menu__content-alt-trigger',
      );
      let isExpanded;

      /**
       * Resolve first click.
       */
      function resolveFirstClick() {
        simulateEvent('click', subTrigger);

        window.setTimeout(resolveSecondClick, 200);
      }

      /**
       * Resolve second click.
       */
      function resolveSecondClick() {
        simulateEvent('click', subAltTrigger);

        window.setTimeout(resolveThirdClick, 200);
      }

      /**
       * Resolve third click.
       */
      function resolveThirdClick() {
        isExpanded = secondPanel.getAttribute('data-open');

        expect(isExpanded).toEqual('false');
        done();
      }

      simulateEvent('click', menuTrigger);

      window.setTimeout(resolveFirstClick, 200);
    });
  });
});
