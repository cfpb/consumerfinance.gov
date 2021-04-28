import {
  expandableView
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/expandable';
import Expandable from '@cfpb/cfpb-expandables/src/Expandable';

const HTML = `
  <div class="o-expandable">
    <button class="o-expandable_header o-expandable_target" title="Expand content">
      <h3 class="h4 o-expandable_header-left o-expandable_label">
        Expandable
      </h3>
    </button>
    <div class="o-expandable_content"><div class="yes-route-details"></div></div>
  </div>
`;

describe( 'expandableView', () => {
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
      expandable = expandables[0];
      target = expandable.element.querySelector( '.o-expandable_target' );
      view = expandableView( expandable.element, {
        expandable
      } );
      view.init();
    } );

    afterEach( () => {
      expandables.length = 0;
      view = null;
    } );


    it( 'adds route-details section as a direct child when closed', () => {
      target.click();
      // The expandable starts open, so click it again.
      target.click();
      const children = expandable.element.children;

      expect( children.length ).toBe( 3 );
      expect( children[2].outerHTML ).toBe(
        '<div class="yes-route-details o-expandable_content"></div>'
      );
    } );

    it( 'removes route-details section as a direct child when re-opened', () => {
      target.click();
      target.click();
      target.click();

      expect( expandable.element.children.length ).toBe( 2 );
    } );
  } );
} );
