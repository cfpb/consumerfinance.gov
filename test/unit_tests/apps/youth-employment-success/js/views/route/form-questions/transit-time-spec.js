import { simulateEvent } from '../../../../../../../util/simulate-event';
import
transitTimeView
  // eslint-disable-next-line max-len
  from '../../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/route/form-questions/transit-time';
import {
  updateTimeToActionPlan,
  updateTransitTimeHoursAction,
  updateTransitTimeMinutesAction
// eslint-disable-next-line max-len
} from '../../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';
import TODO_FIXTURE from '../../../../fixtures/todo-alert';
import mockStore from '../../../../../../mocks/store';
import TodoNotificationMock from '../../../../mocks/todo-notification';

const CLASSES = transitTimeView.CLASSES;

const HTML = `
  <div class="content-l content-l_col-2-3 block__sub-micro m-yes-transit-time">
    <div class="form-l_col form-l_col-1-4">
      <input class="${ CLASSES.HOURS }" type="text" value="" data-js-name="transitTimeHours">
    </div>
    <div class="form-l_col form-l_col-1-4">
      <input class="${ CLASSES.MINUTES }" type="text" value="" data-js-name="transitTimeMinutes">
    </div>
    <div class="m-form-field m-form-field__checkbox block__sub-micro">
      <input class="a-checkbox ${ CLASSES.NOT_SURE }" type="checkbox" name="timeToActionPlan">
      <label class="a-label" for="input_37ad90bd3b546a_i'm-not-sure-add-this-to-my-to-do-list-to-look-up-later-">
        <span>I'm not sure, add this to my to-do list to look up later </span>
      </label>
    </div>
  </div>
  ${ TODO_FIXTURE }
`;

describe( 'transitTimeView', () => {
  const routeIndex = 0;
  const todoNotification = new TodoNotificationMock();
  const dispatch = jest.fn();
  let el;
  let view;
  let store;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    store = mockStore();
    el = document.querySelector( `.${ CLASSES.CONTAINER }` );
    view = transitTimeView( el, { store, routeIndex, todoNotification } );
    view.init();
  } );

  afterEach( () => {
    store.mockReset();
    todoNotification.mockReset();
    dispatch.mockReset();
    view = null;
  } );

  it( 'subscribes to the store on init', () => {
    expect( store.subscribe.mock.calls.length ).toBe( 1 );
  } );

  it( 'dispatches correct action when hours field is changed', () => {
    const hoursEl = document.querySelector(
      '[data-js-name="transitTimeHours"]'
    );
    const hours = '1';

    hoursEl.value = hours;

    simulateEvent( 'blur', hoursEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateTransitTimeHoursAction( {
        routeIndex, value: hours
      } )
    );
  } );

  it( 'dispatches correct event when minutes field is updated', () => {
    const minutesEl = document.querySelector(
      '[data-js-name="transitTimeMinutes"]'
    );
    const minutes = '20';

    minutesEl.value = minutes;

    simulateEvent( 'blur', minutesEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateTransitTimeMinutesAction( {
        routeIndex, value: minutes
      } )
    );
  } );

  it( 'dispatches correct event when not sure checkbox is clicked', () => {
    const checkboxEl = document.querySelector( '[name="timeToActionPlan"]' );

    simulateEvent( 'click', checkboxEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateTimeToActionPlan( {
        routeIndex, value: true
      } )
    );
  } );

  it( 'initializes todo notification component on init', () => {
    expect( todoNotification.init.mock.calls.length ).toBe( 1 );
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

  it( 'updates minutes field when current state has changed', () => {
    const state = {
      routes: {
        routes: [ {
          transitTimeMinutes: '0'
        } ]
      }
    };
    const minutesEl = el.querySelector( `.${ CLASSES.MINUTES }` );
    minutesEl.value = '';

    store.subscriber()( { routes: { routes: [ {} ]}}, state );

    expect( minutesEl.value ).toBe( '0' );
  } );

  it( 'updates hours field when current state has changed', () => {
    const state = {
      routes: {
        routes: [ {
          transitTimeHours: '0'
        } ]
      }
    };
    const hoursEl = el.querySelector( `.${ CLASSES.HOURS }` );
    hoursEl.value = '';

    store.subscriber()( { routes: { routes: [ {} ]}}, state );

    expect( hoursEl.value ).toBe( '0' );
  } );
} );
