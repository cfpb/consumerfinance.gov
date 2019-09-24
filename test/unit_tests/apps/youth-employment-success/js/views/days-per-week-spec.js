import { simulateEvent } from '../../../../../util/simulate-event';
import daysPerWeekView from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/days-per-week';
import {
  clearDaysPerWeekAction,
  updateDaysPerWeekAction,
  updateDaysToActionPlan
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';

const HTML = `
  <div class="m-yes-days-per-week">
    <input type="text" name="daysPerWeek" data-js-name="daysPerWeek">
    <input type="checkbox" name="yes-route-days-unsure">
  </div>
`;

describe( 'DaysPerWeekView', () => {
  const routeIndex = 0;
  const CLASSES = daysPerWeekView.CLASSES;
  const dispatch = jest.fn();
  function mockStore() {
    let subscriberFn;

    return {
      subscriber() {
        return subscriberFn;
      },
      dispatch,
      subscribe: jest.fn().mockImplementation( fn => {
        subscriberFn = fn;
      } )
    };
  }
  let store;
  let view;
  let dom;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    store = mockStore();
    dom = document.querySelector( `.${ CLASSES.CONTAINER }` );
    view = daysPerWeekView( dom, { store, routeIndex } );
    view.init();
  } );

  afterEach( () => {
    dispatch.mockReset();
    view = null;
    store = null;
  } );

  describe( 'on initialize', () => {
    it( 'hides its container element', () => {
      expect( dom.classList.contains( 'u-hidden' ) ).toBeTruthy();
    } );

    it( 'subscribes to the store', () => {
      expect( store.subscribe ).toHaveBeenCalled();
    } );
  } );

  describe( 'event handling', () => {
    it( 'calls the correct action on text input', () => {
      const daysEl = dom.querySelector( 'input[type="text"]' );
      const daysPerWeek = '2';
      const mock = store.dispatch.mock;

      daysEl.value = daysPerWeek;

      simulateEvent( 'input', daysEl );

      expect( mock.calls.length ).toBe( 1 );
      expect( mock.calls[0][0] ).toEqual(
        updateDaysPerWeekAction( {
          routeIndex,
          value: daysPerWeek
        } )
      );
    } );

    it( 'calls the correct action on checkbox input', () => {
      const notSureEl = dom.querySelector( 'input[type="checkbox"]' );
      const mock = store.dispatch.mock;

      notSureEl.checked = 'false';
      simulateEvent( 'click', notSureEl );

      expect( mock.calls.length ).toBe( 1 );
      expect( mock.calls[0][0] ).toEqual(
        updateDaysToActionPlan( {
          routeIndex,
          value: false
        } )
      );
    } );
  } );

  describe( 'on state update', () => {
    it( 'removes u-hidden class when transportation mode is drive', () => {
      const state = {
        routes: {
          routes: [ {
            transportation: 'Drive'
          } ]
        }
      };

      store.subscriber()( { routes: { routes: [ {} ]}}, state );

      expect( dom.classList.contains( 'u-hidden' ) ).toBeFalsy();
    } );

    describe( 'when transportation mode is not Drive', () => {
      const days = '2';
      const checked = 'checked';
      const prevState = {
        routes: {
          routes: [ {
            daysPerWeek: days
          } ]
        }
      };
      const state = {
        routes: {
          routes: [ {
            transportation: 'Walk'
          } ]
        }
      };

      it( 'clears the form inputs', () => {
        const daysEl = dom.querySelector( 'input[type="text"]' );
        const notSureEl = dom.querySelector( 'input[type="checkbox"]' );

        daysEl.value = days;
        notSureEl.checked = checked;

        store.subscriber()( prevState, state );

        expect( daysEl.value ).toBe( '' );
        expect( notSureEl.checked ).toBe( false );
      } );

      it( 'hides the container element, if not hidden', () => {
        const subscriberFn = store.subscriber();
        subscriberFn( prevState, state );

        expect( dom.classList.contains( 'u-hidden' ) ).toBeTruthy();

        subscriberFn( { routes: { routes: [ {} ]}}, {
          routes: {
            routes: [ {
              transportation: 'Drive'
            } ]
          }
        } );

        expect( dom.classList.contains( 'u-hidden' ) ).toBeFalsy();

        subscriberFn( prevState, state );

        expect( dom.classList.contains( 'u-hidden' ) ).toBeTruthy();
      } );

      it( 'dispatches the correct action when daysPerWeek is filled in and transportation method is not drive', () => {
        const mock = store.dispatch.mock;
        store.subscriber()( prevState, state );

        expect( mock.calls.length ).toBe( 1 );
        expect( mock.calls[0][0] ).toEqual(
          clearDaysPerWeekAction( { routeIndex } )
        );
      } );
    } );
  } );
} );
