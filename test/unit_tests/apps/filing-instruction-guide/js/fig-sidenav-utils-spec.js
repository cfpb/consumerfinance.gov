import {
  init as figeSidenavUtilsInit,
  appRoot,
  navItems,
  navItemContainers,
  highlightNavItem,
  unHighlightNavItem,
} from '../../../../../cfgov/unprocessed/apps/filing-instruction-guide/js/fig-sidenav-utils.js';

import HTML_SNIPPET from '../fixtures/sample-fig-page.js';

describe('The Filing Instruction Guide side navigation', () => {
  describe('Table of contents', () => {
    beforeEach(() => {
      // Load HTML fixture
      document.body.innerHTML = HTML_SNIPPET;
      figeSidenavUtilsInit();
    });

    it('should find the app root', () => {
      expect(appRoot).toBeTruthy();
    });

    it('should build a list of nav items', () => {
      expect(navItems.size).toEqual(36);
      expect(navItems.get('#1').innerHTML).toContain(
        '1. What is the filing instructions guide?',
      );
      expect(navItems.get('#5').innerHTML).toContain('5. Where to get help');
      expect(navItems.get('#4.2').innerHTML).toContain(
        '4.2. Multi-field errors',
      );
    });

    it('should build a list of nav container items', () => {
      expect(navItemContainers.size).toEqual(36);
    });

    it('should have nav items in the same section have the same containers', () => {
      expect(navItemContainers.size).toEqual(36);
      // Test all seven nav sections
      let i = 7;
      while (i--) {
        // Against each of their subsections
        let n = 26;
        while (n--) {
          if (navItemContainers.get(`#${i}.${n}`)) {
            expect(navItemContainers.get(`#${i}`)).toEqual(
              navItemContainers.get(`#${i}.${n}`),
            );
          }
        }
      }
    });

    it('should highlight nav items', () => {
      highlightNavItem('#4');
      expect(navItems.get('#4').outerHTML).toContain(
        'o-secondary-nav__link--current',
      );
      highlightNavItem('#2');
      expect(navItems.get('#2').outerHTML).toContain(
        'o-secondary-nav__link--current',
      );
      highlightNavItem('#5');
      expect(navItems.get('#5').outerHTML).toContain(
        'o-secondary-nav__link--current',
      );
    });

    it('should unhighlight nav items', () => {
      highlightNavItem('#4');
      unHighlightNavItem('#4');
      expect(navItems.get('#4').outerHTML).not.toContain(
        'o-secondary-nav__link--current',
      );
      highlightNavItem('#2');
      unHighlightNavItem('#2');
      expect(navItems.get('#2').outerHTML).not.toContain(
        'o-secondary-nav__link--current',
      );
      highlightNavItem('#5');
      unHighlightNavItem('#5');
      expect(navItems.get('#5').outerHTML).not.toContain(
        'o-secondary-nav__link--current',
      );
    });
  });
});
