import { simulateEvent } from '../../../../../util/simulate-event';
import averageCostView from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/average-cost';
import {
  clearAverageCostAction,
  updateAverageCostAction,
  updateCostToActionPlan,
  updateIsMonthlyCostAction
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';

const HTML = `
  <div class="content-l content-l_col-2-3 block__sub-micro m-yes-average-cost">
      <div class="form-l_col form-l_col-1-4">
      <label class="a-label a-label__heading u-mb0" for="input_37b566d867b4ec_what's-the-average-cost">
          What's the average cost?</label><p id="input_ht_37b566d867b67e_what's-the-average-cost"><small>If it's free, enter 0</small></p><input id="input_37b566d867b4ec_what's-the-average-cost" name="input_37b566d867b4ec_what's-the-average-cost" type="text" value="" data-js-name="averageCost" aria-describedby="&quot;input_ht_37b566d867b67e_what's-the-average-cost&quot;" class="">
      
    </div>
      <div class="m-form-field m-form-field__radio a-yes-average-cost">
        <input class="a-radio" type="radio" value="daily" id="input_37b566d867baf2_daily" name="average-cost">
        <label class="a-label" for="input_37b566d867baf2_daily">
            Daily
        </label>
    </div>
      <div class="m-form-field m-form-field__radio a-yes-average-cost">
        <input class="a-radio" type="radio" value="monthly" id="input_37b566d867be3a_monthly" name="average-cost">
        <label class="a-label" for="input_37b566d867be3a_monthly">
            Monthly
        </label>
    </div>
      <div class="m-form-field m-form-field__checkbox u-js-only block__sub-micro">
        <input class="a-checkbox" type="checkbox" value="input_37b566d867c130_i'm-not-sure-add-this-to-my-to-do-list-to-look-up-later" id="input_37b566d867c130_i'm-not-sure-add-this-to-my-to-do-list-to-look-up-later" name="yes-miles-unsure">
        <label class="a-label" for="input_37b566d867c130_i'm-not-sure-add-this-to-my-to-do-list-to-look-up-later">
            <span>I'm not sure, add this to my to-do list to look up later</span>
        </label>
    </div>
  </div>
`;

describe( 'averageCostView', () => {
  const routeIndex = 0;
  const CLASSES = averageCostView.CLASSES;
  const dispatch = jest.fn();
  const mockStore = () => ( {
    dispatch,
    subscribe() { return {}; }
  } );
  let store;
  let view;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    store = mockStore();
    view = averageCostView( document.querySelector( `.${ CLASSES.CONTAINER }` ), { store, routeIndex } );
    view.init();
  } );

  afterEach( () => {
    dispatch.mockReset();
    view = null;
    store = null;
  } );

  it( 'dispatches the correct action when average cost input changes', () => {
    const costEl = document.querySelector( 'input[type="text"]' );
    const cost = '12';

    costEl.value = cost;

    simulateEvent( 'input', costEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateAverageCostAction( {
        routeIndex, value: cost
      } )
    );
  } );

  it( 'dispatches the correct action when a radio button is selected', () => {
    const radioEls = document.querySelectorAll( `.${ CLASSES.RADIO }` );
    const dailyEl = radioEls[0];
    const monthlyEl = radioEls[1];

    simulateEvent( 'click', dailyEl );
    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateIsMonthlyCostAction( {
        routeIndex, value: false
      } )
    );

    simulateEvent( 'click', monthlyEl );

    expect( mock.calls.length ).toBe( 2 );
    expect( mock.calls[1][0] ).toEqual(
      updateIsMonthlyCostAction( {
        routeIndex, value: true
      } )
    );
  } );

  it( 'dispatches the correct action when not sure checkbox is clicked', () => {
    const notSureEl = document.querySelector( 'input[type="checkbox"]' );

    simulateEvent( 'click', notSureEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateCostToActionPlan( {
        routeIndex, value: true
      } )
    );
  } );
} );
