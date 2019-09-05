import { simulateEvent } from '../../../../../util/simulate-event';
import transitTimeView from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/transit-time';
import {
  updateTimeToActionPlan,
  updateTransitTimeHoursAction,
  updateTransitTimeMinutesAction
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';

const HTML = `
  <div class="content-l content-l_col-2-3 block__sub-micro m-yes-transit-time">
    <div class="form-l_col form-l_col-1-4">
      <label class="a-label a-label__heading u-mb0" for="input_37ad90bd3b4790_hours">
        Hours
      </label>
      <input id="input_37ad90bd3b4790_hours" name="input_37ad90bd3b4790_hours" type="text" value="" data-js-name="transitTimeHours">
    </div>
    <div class="form-l_col form-l_col-1-4">
      <label class="a-label a-label__heading u-mb0" for="input_37ad90bd3b4ed4_minutes">
        Minutes
      </label>
      <input id="input_37ad90bd3b4ed4_minutes" name="input_37ad90bd3b4ed4_minutes" type="text" value="" data-js-name="transitTimeMinutes">
      
    </div>
    <div class="m-form-field m-form-field__checkbox block__sub-micro">
      <input class="a-checkbox" type="checkbox" value="input_37ad90bd3b546a_i'm-not-sure-add-this-to-my-to-do-list-to-look-up-later-" id="input_37ad90bd3b546a_i'm-not-sure-add-this-to-my-to-do-list-to-look-up-later-" name="timeToActionPlan">
      <label class="a-label" for="input_37ad90bd3b546a_i'm-not-sure-add-this-to-my-to-do-list-to-look-up-later-">
        <span>I'm not sure, add this to my to-do list to look up later </span>
      </label>
    </div>
  </div>
`;

describe( 'transitTimeView', () => {
  const routeIndex = 0;
  const CLASSES = transitTimeView.CLASSES;
  const dispatch = jest.fn();
  const mockStore = () => ( {
    dispatch,
    subscribe() { return {}; }
  } );
  let view;
  let store;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    store = mockStore();
    view = transitTimeView( document.querySelector( `.${ CLASSES.CONTAINER }` ), { store, routeIndex } );
    view.init();
  } );

  afterEach( () => {
    dispatch.mockReset();
    view = null;
  } );

  it( 'dispatches the correct event when hours field is changed', () => {
    const hoursEl = document.querySelector( '[data-js-name="transitTimeHours"]' );
    const hours = '1';

    hoursEl.value = hours;

    simulateEvent( 'input', hoursEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateTransitTimeHoursAction( {
        routeIndex, value: hours
      } )
    );
  } );

  it( 'dispatches the correct event when the minutes field is updated', () => {
    const minutesEl = document.querySelector( '[data-js-name="transitTimeMinutes"]' );
    const minutes = '20';

    minutesEl.value = minutes;

    simulateEvent( 'input', minutesEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateTransitTimeMinutesAction( {
        routeIndex, value: minutes
      } )
    );
  } );

  it( 'dispatches the correct event when the not sure checkbox is clicked', () => {
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
} );
