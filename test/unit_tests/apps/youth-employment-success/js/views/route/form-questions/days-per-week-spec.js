import { simulateEvent } from '../../../../../../../util/simulate-event';
import
daysPerWeekView
  // eslint-disable-next-line max-len
  from '../../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/route/form-questions/days-per-week';
import {
  clearDaysPerWeekAction,
  updateDaysPerWeekAction,
  updateDaysToActionPlan
// eslint-disable-next-line max-len
} from '../../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';
import TODO_FIXTURE from '../../../../fixtures/todo-alert';
import TodoNotificationMock from '../../../../mocks/todo-notification';

const HTML = `
  <div class="m-yes-days-per-week">
    <input type="text" name="daysPerWeek" data-js-name="daysPerWeek">
    <input type="checkbox" name="yes-route-days-unsure">
  </div>
  ${ TODO_FIXTURE }
`;

describe( 'DaysPerWeekView', () => {
  const routeIndex = 0;
  const CLASSES = daysPerWeekView.CLASSES;
  const dispatch = jest.fn();
  const todoNotification = new TodoNotificationMock();
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
    view = daysPerWeekView( dom, { store, routeIndex, todoNotification } );
    view.init();
  } );

  afterEach( () => {
    todoNotification.mockReset();
    dispatch.mockReset();
    view = null;
    store = null;
  } );

  describe( 'on initialize', () => {
    it( 'subscribes to the store', () => {
      expect( store.subscribe ).toHaveBeenCalled();
    } );

    it( 'initializes todo notification component on init', () => {
      expect( todoNotification.init.mock.calls.length ).toBe( 1 );
    } );
  } );

  describe( 'event handling', () => {
    it( 'calls correct action on text input', () => {
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

    it( 'calls correct action on checkbox input', () => {
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

    it( 'toggles notifications when checkbox is clicked', () => {
      const notSureEl = document.querySelector( 'input[type="checkbox"]' );

      simulateEvent( 'click', notSureEl );

      expect( todoNotification.show.mock.calls.length ).toBe( 1 );
      expect( todoNotification.hide.mock.calls.length ).toBe( 0 );

      notSureEl.checked = true;

      simulateEvent( 'click', notSureEl );

      expect( todoNotification.show.mock.calls.length ).toBe( 1 );
      expect( todoNotification.hide.mock.calls.length ).toBe( 1 );
    } );
  } );

  describe( 'on state update', () => {
    it( 'removes u-hidden class when transportation mode is drive', () => {
      const state = {
        routes: {
          routes: [ {
            transportation: 'Drive',
            actionPlanItems: []
          } ]
        }
      };

      store.subscriber()( { routes: { routes: [ {} ]}}, state );

      expect( dom.classList.contains( 'u-hidden' ) ).toBeFalsy();
    } );

    describe( 'when average cost is defined as a monthly cost', () => {
      const days = '2';
      const checked = 'checked';
      const prevState = {
        routes: {
          routes: [ {
            daysPerWeek: days,
            actionPlanItems: []
          } ]
        }
      };
      const state = {
        routes: {
          routes: [ {
            transportation: 'Walk',
            isMonthlyCost: true,
            actionPlanItems: []
          } ]
        }
      };

      it( 'clears form inputs', () => {
        const daysEl = dom.querySelector( 'input[type="text"]' );
        const notSureEl = dom.querySelector( 'input[type="checkbox"]' );

        daysEl.value = days;
        notSureEl.checked = checked;

        store.subscriber()( prevState, state );

        expect( daysEl.value ).toBe( '' );
        expect( notSureEl.checked ).toBe( false );
      } );

      it( 'hides container element if not hidden', () => {
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

      it( 'dispatches correct action when daysPerWeek is filled in', () => {
        const mock = store.dispatch.mock;
        store.subscriber()( prevState, state );

        expect( mock.calls.length ).toBe( 1 );
        expect( mock.calls[0][0] ).toEqual(
          clearDaysPerWeekAction( { routeIndex } )
        );
      } );

      it( 'calls .remove on todo notification ' +
          'component when this view is toggled', () => {
        store.subscriber()( { routes: { routes: [ {} ]}}, state );

        expect( todoNotification.remove.mock.calls.length ).toBe( 1 );
      } );
    } );
  } );
} );
