import { simulateEvent } from '../../../../util/simulate-event';
import addRouteOptionView from '../../../../../cfgov/unprocessed/apps/youth-employment-success/js/add-route-option-view';

const HTML = `
  <button class="${ addRouteOptionView.CLASSES.BUTTON }"></buton>
`;

const clickHandlerMock = jest.fn();

describe( 'addRouteOptionView', () => {
  let view;
  let el;

  beforeEach( () => {
    document.body.innerHTML = HTML;

    el = document.querySelector( `.${ addRouteOptionView.CLASSES.BUTTON }` );
    view = addRouteOptionView( el, { onAddExpandable: clickHandlerMock } );
    view.init();
  } );

  it( 'calls onAddExpandable function prop on click', () => {
    simulateEvent( 'click', el );

    expect( clickHandlerMock.mock.calls.length ).toBe( 1 );
  } );

  it( 'throws an error when the view is initialized without its function handler', () => {
    expect( () => addRouteOptionView( el ) ).toThrow();

    expect( () => addRouteOptionView( el, { onAddExpandable: 'foo' } ) ).toThrow();
  } );
} );
