import { simulateEvent } from '../../../../util/simulate-event';
import routeOptionFormView from '../../../../../cfgov/unprocessed/apps/youth-employment-success/js/route-option-view';
import {
  updateDailyCostAction,
  updateDaysPerWeekAction,
  updateMilesAction,
  updateTransportationAction
} from '../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';

const HTML = `
  <form class="o-yes-route-option">
    <input type="text" name="miles" data-js-name="miles" class="a-yes-question">
    <input type="text" name="dailyCost" data-js-name="dailyCost" class="a-yes-question">
    <input type="text" name="daysPerWeek" data-js-name="daysPerWeek" class="a-yes-question">
    <input type="text" name="averageCost" data-js-name="averageCost" class="a-yes-question">
    <input type="radio" name="transpo" class="a-yes-route-mode" value="Bus">
    <input type="radio" name="transpo" class="a-yes-route-mode" value="Drive">
    <div class="m-yes-transit-time"></div>
  </form>
`;

describe( 'routeOptionFormView', () => {
  const CLASSES = routeOptionFormView.CLASSES;
  const dispatch = jest.fn();
  const mockStore = () => ( {
    dispatch,
    subscribe( fn ) {
      return fn( {
        routes: { routes: []}
      }, {
        routes: { routes: []
        }
      } );
    },
    getState() {
      return {
        routes: {
          routes: []
        }
      };
    }
  } );
  let view;
  let store;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    store = mockStore();
    view = routeOptionFormView( document.querySelector( `.${ CLASSES.FORM }` ), { store, routeIndex: 0 } );
    view.init();
  } );

  afterEach( () => {
    dispatch.mockReset();
    view = null;
  } );

  it( 'dispatches an action to update `miles` input', () => {
    const milesEl = document.querySelector( 'input[name="miles"]' );
    const value = '12';

    milesEl.value = value;

    simulateEvent( 'input', milesEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual( updateMilesAction( {
      routeIndex: 0,
      value } ) );
  } );

  it( 'dispatches an action to update `dailyCost` input', () => {
    const dailyCostEl = document.querySelector( 'input[name="dailyCost"]' );
    const value = '200';

    dailyCostEl.value = value;

    simulateEvent( 'input', dailyCostEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual( updateDailyCostAction( { routeIndex: 0, value } ) );
  } );

  it( 'dispatches an action to update `daysPerWeek` input', () => {
    const daysPerWeekEl = document.querySelector( 'input[name="daysPerWeek"]' );
    const value = '4';

    daysPerWeekEl.value = value;

    simulateEvent( 'input', daysPerWeekEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual( updateDaysPerWeekAction( { routeIndex: 0, value } ) );
  } );

  it( 'dispatches an action to update `transportation` with checkbox selection', () => {
    const radioEl = document.querySelectorAll( 'input[name="transpo"]' )[0];

    simulateEvent( 'click', radioEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual( updateTransportationAction( { routeIndex: 0, value: radioEl.value } ) );
  } );

  describe( 'conditional fields', () => {
    it( 'hides conditional fields on init', () => {
      const averageCostEl = document.querySelector( 'input[name="averageCost"]' );
      const milesEl = document.querySelector( 'input[name="miles"]' );
      const daysPerWeekEl = document.querySelector( 'input[name="daysPerWeek"]' );

      expect( averageCostEl.classList.contains( 'u-hidden' ) ).toBeTruthy();
      expect( milesEl.classList.contains( 'u-hidden' ) ).toBeTruthy();
      expect( daysPerWeekEl.classList.contains( 'u-hidden' ) ).toBeTruthy();
    } );
  } );
} );
