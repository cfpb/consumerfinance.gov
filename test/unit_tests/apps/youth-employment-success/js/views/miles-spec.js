import { simulateEvent } from '../../../../../util/simulate-event';
import milesView from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/miles';
import mockStore from '../../../../mocks/store';
import {
  clearMilesAction,
  updateMilesAction,
  updateMilesToActionPlan
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';
import { PLAN_TYPES } from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/data/todo-items';

const HTML = `
  <div class="m-yes-miles">
    <input type="text">
    <input type="checkbox">
  </div>
`;

describe( 'milesView', () => {
  const routeIndex = 0;
  let store;
  let dom;
  let view;

  beforeEach( () => {
    store = mockStore();
    document.body.innerHTML = HTML;
    dom = document.querySelector( `.${ milesView.CLASSES.CONTAINER }` );
    view = milesView( dom, { store, routeIndex } );
    view.init();
  } );

  afterEach( () => {
    store.mockReset();
    view = null;
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
    it( 'calls the correct action on `miles` field input', () => {
      const milesEl = dom.querySelector( 'input[type="text"]' );
      const milesPerDay = '5';
      const mock = store.dispatch.mock;

      milesEl.value = milesPerDay;

      simulateEvent( 'input', milesEl );

      expect( mock.calls.length ).toBe( 1 );
      expect( mock.calls[0][0] ).toEqual(
        updateMilesAction( {
          routeIndex,
          value: milesPerDay
        } )
      );
    } );

    it( 'calls the correct action when the `not sure` checkbox is clicked', () => {
      const notSureEl = document.querySelector( 'input[type="checkbox"]' );
      const mock = store.dispatch.mock;

      simulateEvent( 'click', notSureEl );

      expect( mock.calls.length ).toBe( 1 );
      expect( mock.calls[0][0] ).toEqual(
        updateMilesToActionPlan( {
          routeIndex,
          value: true
        } )
      );
    } );
  } );

  describe( 'on state update', () => {
    it( 'removes u-hidden class when transportation mode is Drive', () => {
      const state = {
        routes: {
          routes: [ {
            transportation: 'Drive'
          } ]
        }
      };

      store.subscriber()( { routes: { routes: [ {} ]} }, state );

      expect( dom.classList.contains( 'u-hidden' ) ).toBeFalsy();
    } );

    describe( 'when transportation mode is not Drive', () => {
      const miles = '12';
      const checked = true;
      const prevState = {
        routes: {
            routes: [ {
            miles: miles
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
        const milesEl = dom.querySelector( 'input[type="text"]' );
        const notSureEl = dom.querySelector( 'input[type="checkbox"]' );

        milesEl.value = miles;
        notSureEl.checked = checked;

        store.subscriber()( prevState, state );

        expect( milesEl.value ).toBe( '' );
        expect( notSureEl.checked ).toBe( false );
      } );

      it( 'hides the container element', () => {
        const subscriberFn = store.subscriber();
        subscriberFn( prevState, state );

        subscriberFn( { routes: { routes: [ {} ]} }, {
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
          clearMilesAction( { routeIndex } )
        );
      } );

      it( 'dispatches the correct action when not sure is selected and transportation method is not drive', () => {
        const mock = store.dispatch.mock;
        store.subscriber()( {
          routes: {
            routes: [ {
              actionPlanItems: [ PLAN_TYPES.MILES ]
            } ]
          }
        }, state );

        expect( mock.calls.length ).toBe( 1 );
        expect( mock.calls[0][0] ).toEqual(
          clearMilesAction( { routeIndex } )
        );
      } );
    } );
  } );
} );
