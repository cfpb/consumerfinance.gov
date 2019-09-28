import { simulateEvent } from '../../../../../util/simulate-event';
import printButton from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/print-button';

const CLASSES = printButton.CLASSES;
const HTML = `<button class="${ CLASSES.BUTTON }"></button>`;

describe( 'printButtonView', () => {
  const printMock = jest.fn();
  let dom;

  beforeEach( () => {
    window.print = printMock;
    document.body.innerHTML = HTML;
    dom = document.querySelector( `.${ CLASSES.BUTTON }` );
    printButton( dom ).init();
  } );

  it( 'calls the system print dialog when clicked', () => {
    simulateEvent( 'click', dom );

    expect( printMock.mock.calls.length ).toBe( 1 );
  } );
} );
