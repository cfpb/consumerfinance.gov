import { simulateEvent } from '../../../../../../util/simulate-event';
import
routeOptionToggleView
  // eslint-disable-next-line max-len
  from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/route/option-toggle';

const HTML = `
  <button class="${ routeOptionToggleView.CLASSES.BUTTON }"></buton>
`;

const initMock = jest.fn();
const mockExpandable = () => ( {
  element: ( () => {
    const container = document.createElement( 'div' );
    const target = document.createElement( 'div' );


    target.classList.add( 'o-expandable_target' );
    container.classList.add( 'u-hidden' );

    container.appendChild( target );

    return container;
  } )()
} );
const mockRouteForm = {
  init: initMock
};

describe( 'routeOptionToggleView', () => {
  let expandable;
  let view;
  let el;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    expandable = mockExpandable();

    el = document.querySelector(
      `.${ routeOptionToggleView.CLASSES.BUTTON }`
    );
    view = routeOptionToggleView( el, {
      expandable,
      routeOptionForm: mockRouteForm
    } );

    mockRouteForm.init.mockReset();

    view.init();
  } );

  it( 'hides itself on click', () => {
    simulateEvent( 'click', el );

    expect( el.classList.contains( 'u-hidden' ) ).toBeTruthy();
  } );

  it( 'shows its expandable on click', () => {
    expect( expandable.element.classList.contains( 'u-hidden' ) ).toBeTruthy();

    simulateEvent( 'click', el );

    expect( expandable.element.classList.contains( 'u-hidden' ) ).toBeFalsy();
  } );

  it( 'calls .init on associated route form', () => {
    expect( mockRouteForm.init.mock.calls.length ).toBe( 0 );
    simulateEvent( 'click', el );
    expect( mockRouteForm.init.mock.calls.length ).toBe( 1 );
  } );
} );
