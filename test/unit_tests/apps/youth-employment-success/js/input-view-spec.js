import
inputView
  // eslint-disable-next-line max-len
  from '../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/input';
import { simulateEvent } from '../../../../util/simulate-event';

const HTML = `
  <div>
    <input type="text" name="my-input">
  </div>
`;

describe( 'InputView', () => {
  let view;

  beforeEach( () => {
    document.body.innerHTML = HTML;
  } );

  afterEach( () => {
    view = null;
  } );

  it( 'sets an initialized flag on the root node', () => {
    view = inputView( document.querySelector( 'div' ) );
    view.init();

    expect( document.querySelector( 'div' )
      .getAttribute( 'data-js-hook' )
    ).toBeTruthy();
  } );

  it( 'throws an error when an input node matching ' +
      'the `type` prop cannot be found', () => {
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
      change: mockHandler,
      blur: mockHandler
    };
    let eventTarget;

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

    describe( 'sanitizing data', () => {
      it( 'removes data that is not valid ' +
          'when `data-sanitize` attribute is present', () => {
        document.body.innerHTML = `
          <input type="text" data-sanitize="money">
        `;

        const input = document.querySelector( 'input' );
        inputView( input, { events } ).init();

        input.value = '-122';

        simulateEvent( 'change', input );

        expect( input.value ).toBe( '122' );
        expect( mockHandler.mock.calls[0][0].value ).toBe( '122' );
      } );

      it( 'returns original value if type of input is not text', () => {
        document.body.innerHTML = `
          <input type="number">
        `;

        const input = document.querySelector( 'input' );

        inputView( input, { events, type: 'number' } ).init();

        input.value = 12;

        simulateEvent( 'blur', input );

        expect( input.value ).toBe( '12' );
        expect( mockHandler.mock.calls[0][0].value ).toBe( '12' );
      } );

      it( 'returns original value if input is text ' +
          'but there is no pattern', () => {
        document.body.innerHTML = `
          <input type="text">
        `;

        const input = document.querySelector( 'input' );

        inputView( input, { events } ).init();

        input.value = '-1';

        simulateEvent( 'blur', input );

        expect( input.value ).toBe( '-1' );
        expect( mockHandler.mock.calls[0][0].value ).toBe( '-1' );
      } );
    } );
  } );
} );
