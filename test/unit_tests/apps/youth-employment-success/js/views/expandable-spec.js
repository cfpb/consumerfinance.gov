import expandableView from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/expandable';
import Expandable from 'cf-expandables/src/Expandable';

const CLASSES = expandableView.CLASSES;

const HTML = `
  <div class="o-expandable">
    <button class="o-expandable_header o-expandable_target" title="Expand content">
      <h3 class="h4 o-expandable_header-left o-expandable_label">
        Option
      </h3>
    </button>
    <div class="o-expandable_content"><div class="yes-route-details"></div></div>
  </div>
`;

describe( 'expandableView', () => {
  const index = 0;
  let expandables;
  let expandable;
  let target;
  let view;

  it( 'throws an error when initialized without an expandable', () => {
    expect( () => expandableView( document.body ) ).toThrow( TypeError );
  } );

  describe( 'proper instantiation', () => {
    beforeEach( () => {
      document.body.innerHTML = HTML;
      expandables = Expandable.init();
      expandable = expandables[index];
      target = expandable.element.querySelector( '.o-expandable_target' );
      view = expandableView( expandable.element, {
        expandable,
        index
      } );
      view.init();
    } );

    afterEach( () => {
      expandables.length = 0;
      view = null;
    } );

    it( 'opens the child expandable on init', () => {
      const contentEl = expandable.element.querySelector( '.o-expandable_content' );

      expect( contentEl.classList.contains( 'o-expandable_content__expanded' ) ).toBeTruthy();
    } );

    it( 'sets the header of the expandable to `Option `index+1`', () => {
      const headingEl = expandable.element.querySelector( `.${ CLASSES.HEADING }` );

      expect( headingEl.textContent ).toBe( 'Option 1' );
    } );

    it( 'adds the route-details section as a direct child when closed', () => {
      target.click();
      const children = expandable.element.children;

      expect( children.length ).toBe( 3 );
      expect( children[2].outerHTML ).toBe(
        '<div class="yes-route-details o-expandable_content"></div>'
      );
    } );

    it( 'removes the route-details section as a direct child when re-opened', () => {
      target.click();
      target.click();

      expect( expandable.element.children.length ).toBe( 2 );
    } );
  } );
} );
