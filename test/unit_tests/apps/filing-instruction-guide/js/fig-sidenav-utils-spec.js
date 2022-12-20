import HTML_SNIPPET from '../fixtures/sample-fig-page.js';
import {
  init as figeSidenavUtilsInit,
  appRoot,
  navItems,
  navItemContainers,
  highlightNavItem,
  unHighlightNavItem,
} from '../../../../../cfgov/unprocessed/apps/filing-instruction-guide/js/fig-sidenav-utils.js';

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
      expect(navItems.size).toEqual(40);
      expect(navItems.get('#1').innerHTML).toContain('What is the FIG?');
      expect(navItems.get('#5').innerHTML).toContain('Data validation');
      expect(navItems.get('#4.2').innerHTML).toContain('Application Date');
    });

    it('should build a list of nav container items', () => {
      expect(navItemContainers.size).toEqual(40);
    });

    it('should have nav items in the same section have the same containers', () => {
      expect(navItemContainers.size).toEqual(40);
      // Test all seven nav sections
      let i = 7;
      while (i--) {
        // Against each of their subsections
        let n = 26;
        while (n--) {
          if (navItemContainers.get(`#${i}.${n}`)) {
            expect(navItemContainers.get(`#${i}`)).toEqual(
              navItemContainers.get(`#${i}.${n}`)
            );
          }
        }
      }
    });

    it('should highlight nav items', () => {
      highlightNavItem('#4');
      expect(navItems.get('#4').outerHTML).toContain('m-nav-link__current');
      highlightNavItem('#2');
      expect(navItems.get('#2').outerHTML).toContain('m-nav-link__current');
      highlightNavItem('#5');
      expect(navItems.get('#5').outerHTML).toContain('m-nav-link__current');
    });

    it('should unhighlight nav items', () => {
      highlightNavItem('#4');
      unHighlightNavItem('#4');
      expect(navItems.get('#4').outerHTML).not.toContain(
        'm-nav-link__current'
      );
      highlightNavItem('#2');
      unHighlightNavItem('#2');
      expect(navItems.get('#2').outerHTML).not.toContain(
        'm-nav-link__current'
      );
      highlightNavItem('#5');
      unHighlightNavItem('#5');
      expect(navItems.get('#5').outerHTML).not.toContain(
        'm-nav-link__current'
      );
    });
  });
});
