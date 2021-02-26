import { simulateEvent } from '../../../../../../util/simulate-event';
import routeOptionFormView from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/route/option-form';
import {
  averageCostView,
  daysPerWeekView,
  drivingCostEstimateView,
  milesView,
  transitTimeView
} from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/route/form-questions';
import routeDetailsView from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/route/details';
import { updateTransportationAction } from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';
import mockStore from '../../../../../mocks/store';

jest.mock(
  '../../../../../../../cfgov/unprocessed/apps/' +
  'youth-employment-success/js/views/todo-notification'
);

const CLASSES = routeOptionFormView.CLASSES;
const HTML = `
  <form class="o-yes-route-option">
    <input type="text" name="miles" data-js-name="miles" class="a-yes-question">
    <div class="m-yes-average-cost">
      <input type="text" name="averageCost" data-js-name="averageCost" class="a-yes-question">
    </div>
    <input type="text" name="daysPerWeek" data-js-name="daysPerWeek" class="a-yes-question">
    <input type="text" name="averageCost" data-js-name="averageCost" class="a-yes-question">
    <input type="radio" name="transpo" class="a-yes-route-mode" value="Bus">
    <input type="radio" name="transpo" class="a-yes-route-mode" value="Drive">
    <div class="${ CLASSES.DISCOUNT }"></div>
    <div class="m-yes-transit-time"></div>
    <div class="yes-route-details"></div>
  </form>
`;

describe( 'routeOptionFormView', () => {
  const dispatch = jest.fn();
  const detailsInit = jest.fn();
  const detailsRender = jest.fn();
  const costEstimateInit = jest.fn();
  const costEstimateRender = jest.fn();
  const costViewInit = jest.fn();
  const daysViewInit = jest.fn();
  const milesViewInit = jest.fn();
  const transitViewInit = jest.fn();
  const detailsView = () => ( {
    init: detailsInit,
    render: detailsRender
  } );
  detailsView.CLASSES = routeDetailsView.CLASSES;
  const costEstimateView = () => ( {
    init: costEstimateInit,
    render: costEstimateRender
  } );
  costEstimateView.CLASSES = drivingCostEstimateView.CLASSES;
  const viewMock = mock => () => ( {
    init: mock
  } );
  const costViewMock = viewMock( costViewInit );
  costViewMock.CLASSES = averageCostView.CLASSES;

  const daysPerWeekViewMock = viewMock( daysViewInit );
  daysPerWeekViewMock.CLASSES = daysPerWeekView.CLASSES;

  const milesViewMock = viewMock( milesViewInit );
  milesViewMock.CLASSES = milesView.CLASSES;

  const transitViewMock = viewMock( transitViewInit );
  transitViewMock.CLASSES = transitTimeView.CLASSES;

  let view;
  let store;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    store = mockStore();
    view = routeOptionFormView(
      document.querySelector( `.${ CLASSES.FORM }` ),
      {
        store,
        routeIndex: 0,
        routeDetailsView: detailsView,
        averageCostView: costViewMock,
        daysPerWeekView: daysPerWeekViewMock,
        drivingCostEstimateView: costEstimateView,
        milesView: milesViewMock,
        transitTimeView: transitViewMock
      }
    );
    view.init();
  } );

  afterEach( () => {
    store.mockReset();
    dispatch.mockReset();
    view = null;
  } );

  it( 'initializes its children', () => {
    expect( costViewInit ).toHaveBeenCalled();
    expect( detailsInit ).toHaveBeenCalled();
    expect( costEstimateInit ).toHaveBeenCalled();
    expect( daysViewInit ).toHaveBeenCalled();
    expect( milesViewInit ).toHaveBeenCalled();
  } );

  it( 'subscribes to the store on init', () => {
    expect( store.subscribe.mock.calls.length ).toBe( 1 );
  } );

  it( 'dispatches an action to update `transportation` ' +
      'with checkbox selection', () => {
    const radioEl = document.querySelectorAll( 'input[name="transpo"]' )[0];

    simulateEvent( 'click', radioEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateTransportationAction( { routeIndex: 0, value: radioEl.value } )
    );
  } );

  it( 'hides transportation discount section when ' +
      'transportation method is Walk', () => {
    const state = {
      routes: {
        routes: [ {
          transportation: 'Walk'
        } ]
      }
    };
    store.subscriber()( {}, state );

    const discountEl = document.querySelector( `.${ CLASSES.DISCOUNT }` );

    expect( discountEl.classList.contains( 'u-hidden' ) ).toBeTruthy();

    store.subscriber()(
      {}, { routes: { routes: [ { transportation: 'Drive' } ]}}
    );

    expect( discountEl.classList.contains( 'u-hidden' ) ).toBeFalsy();
  } );

  it( 'calls render on the drivingCostEstimateView on state update', () => {
    store.subscriber()( {}, { routes: { routes: [ { } ]}} );

    expect( costEstimateRender ).toHaveBeenCalled();
  } );
} );
