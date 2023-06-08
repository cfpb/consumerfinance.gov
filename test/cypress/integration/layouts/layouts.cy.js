import { onlyOn } from '@cypress/skip-test';

onlyOn('local-machine', () => {
  describe('Site layouts', () => {
    context('across screensizes', () => {
      const devices = ['macbook-15', 'ipad-2', 'iphone-6'];

      devices.forEach((device) => {
        context(device, () => {
          beforeEach(() => {
            cy.viewport(device);
          });

          describe('Homepage', () => {
            it('should display the homepage correctly', () => {
              cy.visit('/');
              cy.compareSnapshot(`home-${device}`);
            });
          });

          describe('Layout 2-1', () => {
            describe('LTR', () => {
              it('should display correctly with breadcrumbs', () => {
                cy.visit('/about-us/blog/');
                cy.compareSnapshot(`layout-2-1-ltr-bc-${device}`);
              });

              it('should display correctly with NO breadcrumbs', () => {
                cy.visit('/compliance/compliance-resources/');
                cy.compareSnapshot(`layout-2-1-ltr-no-bc-${device}`);
              });
            });

            describe('RTL', () => {
              it('should display correctly with breadcrumbs', () => {
                cy.visit('/about-us/blog/hidden-cost-junk-fees-ar/');
                cy.compareSnapshot(`layout-2-1-rtl-bc-${device}`);
              });

              it('should display correctly with NO breadcrumbs', () => {
                cy.visit('/language/ar/');
                cy.compareSnapshot(`layout-2-1-rtl-no-bc-${device}`);
              });

              it('should display correctly with hero', () => {
                cy.visit(
                  '/language/ar/coronavirus/mortgage-and-housing-assistance/'
                );
                cy.compareSnapshot(`layout-2-1-rtl-hero-${device}`);
              });
            });
          });

          describe('Layout 1-3', () => {
            describe('LTR', () => {
              it('should display correctly with breadcrumbs', () => {
                cy.visit('/owning-a-home/prepare/');
                cy.compareSnapshot(`layout-1-3-ltr-bc-${device}`);
              });

              // TODO: FIG has an infinite scroll bug that prevents screenshots on iPhone.
              xit('should display FIG correctly', () => {
                cy.visit(
                  '/data-research/small-business-lending/filing-instructions-guide/2024-guide/'
                );
                cy.compareSnapshot(`layout-1-3-ltr-fig-${device}`);
              });

              it('should display iregs correctly', () => {
                cy.visit('/rules-policy/regulations/1002/');
                cy.compareSnapshot(`layout-1-3-ltr-iregs-${device}`);
              });

              it('should display iregs correctly', () => {
                cy.visit('/consumer-tools/auto-loans/answers/');
                cy.compareSnapshot(`layout-1-3-ltr-iregs-${device}`);
              });
            });

            describe('RTL', () => {
              it('should display correctly with breadcrumbs', () => {
                cy.visit(
                  '/language/ar/coronavirus/mortgage-and-housing-assistance/renter-protections/your-tenant-debt-collection-rights/'
                );
                cy.compareSnapshot(`layout-1-3-rtl-bc-${device}`);
              });
            });
          });
        });
      });
    });
  });
});
