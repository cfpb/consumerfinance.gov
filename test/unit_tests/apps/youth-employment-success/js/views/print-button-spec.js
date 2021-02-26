import { simulateEvent } from '../../../../../util/simulate-event';
import printButton from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/print-button';

const CLASSES = printButton.CLASSES;
const HTML = `
  <div class="${ CLASSES.NO_PRINT }"></div>
  <button class="${ CLASSES.BUTTON }"></button>
`;

describe( 'printButtonView', () => {
  const printMock = jest.fn();
  const printHookMock = jest.fn();
  const onClickMock = jest.fn();
  let addEventSpy;
  let removeEventSpy;
  let dom;
  let view;

  beforeEach( () => {
    window.print = printMock;
    addEventSpy = jest.spyOn( window, 'addEventListener' );
    removeEventSpy = jest.spyOn( window, 'removeEventListener' );
    document.body.innerHTML = HTML;
    dom = document.querySelector( `.${ CLASSES.BUTTON }` );
    view = printButton( dom, { onBeforePrint: printHookMock } );
    view.init();
  } );

  afterEach( () => {
    view = null;
    printMock.mockReset();
  } );

  it( 'calls the system print dialog when clicked', () => {
    simulateEvent( 'click', dom );

    expect( printMock.mock.calls.length ).toBe( 1 );
    expect( addEventSpy ).toHaveBeenCalled();

    simulateEvent( 'focus', window );

    expect( removeEventSpy ).toHaveBeenCalled();
  } );

  it( 'hides elements with the no print class, ' +
      'on print and shows them afterwards', () => {
    const elToToggle = document.querySelector( `.${ CLASSES.NO_PRINT }` );

    expect( elToToggle.classList.contains( CLASSES.HIDE ) ).toBeFalsy();

    simulateEvent( 'click', dom );

    expect( elToToggle.classList.contains( CLASSES.HIDE ) ).toBeTruthy();

    simulateEvent( 'focus', window );

    expect( elToToggle.classList.contains( CLASSES.HIDE ) ).toBeFalsy();
  } );

  it( 'calls its onBeforePrint hook, if provided', () => {
    simulateEvent( 'click', dom );
    expect( printHookMock ).toHaveBeenCalled();
  } );

  it( 'calls its parent click handling function, if supplied', () => {
    document.body.innerHTML = '';
    document.body.innerHTML = HTML;

    dom = document.querySelector( `.${ CLASSES.BUTTON }` );
    view = printButton( dom, { onClick: onClickMock } );
    view.init();

    simulateEvent( 'click', dom );
    expect( onClickMock ).toHaveBeenCalled();
    expect( typeof onClickMock.mock.calls[0][1] === 'function' ).toBeTruthy();
  } );
} );
