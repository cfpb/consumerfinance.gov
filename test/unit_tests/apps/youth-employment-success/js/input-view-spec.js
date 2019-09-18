import inputView from '../../../../../cfgov/unprocessed/apps/youth-employment-success/js/input-view';
import { simulateEvent } from '../../../../util/simulate-event';

const HTML = `
  <div>
    <input type="text" name="my-input">
  </div>
`;

describe( 'InputView', () => {
  let view;
  let docAlias;

  beforeEach( () => {
    document.body.innerHTML = HTML;
  } );

  afterEach( () => {
    view = null;
  } );

  it( 'sets an initialized flag on the root node', () => {
    view = inputView( document.querySelector( 'div' ) );
    view.init();

    expect( document.querySelector( 'div' ).getAttribute( 'data-js-hook' ) ).toBeTruthy();
  } );

  it( 'throws an error when an <input> node matching the `type` prop cannot be found', () => {
    document.body.innerHTML = `
      <div>
        <input type="number">
      </div>
    `;

    expect( () => inputView( document.querySelector( 'div' ) ) ).toThrow();
  } );

  describe( 'event handling', () => {
    const fakeInput = 'hey';
    const mockHandler = jest.fn();
    const events = {
      change: mockHandler
    };
    let eventTarget;
    let view;

    beforeEach( () => {
      const root = document.querySelector( 'div' );
      eventTarget = root.querySelector( 'input' );

      view = inputView( root, { events } );
      view.init();
    } );

    afterEach( () => {
      mockHandler.mockReset();
    } );

    it( 'bind events supplied to it', () => {
      simulateEvent( 'change', eventTarget, { target: { value: fakeInput }} );

      expect( mockHandler.mock.calls.length ).toBe( 1 );
    } );

    it( 'binds events once only', () => {
      view.init();

      simulateEvent( 'change', eventTarget, { target: { value: fakeInput }} );

      expect( mockHandler.mock.calls.length ).toBe( 1 );
    } );
  } );
} );
