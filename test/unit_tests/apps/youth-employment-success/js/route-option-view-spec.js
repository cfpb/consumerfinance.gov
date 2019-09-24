import { simulateEvent } from '../../../../util/simulate-event';
import routeOptionFormView from '../../../../../unprocessed/apps/youth-employment-success/js/route-option-view';
import averageCostView from '../../../../../unprocessed/apps/youth-employment-success/js/views/average-cost';
import milesView from '../../../../../unprocessed/apps/youth-employment-success/js/views/miles';
import {
  updateDaysPerWeekAction,
  updateTransportationAction
} from '../../../../../unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';
import daysPerWeekView from '../../../../../unprocessed/apps/youth-employment-success/js/views/days-per-week';

let UNDEFINED;

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
    <div class="m-yes-transit-time"></div>
    <div class="yes-route-details"></div>
  </form>
`;

describe( 'routeOptionFormView', () => {
  const CLASSES = routeOptionFormView.CLASSES;
  const dispatch = jest.fn();
  const detailsInit = jest.fn();
  const detailsRender = jest.fn();
  const costViewInit = jest.fn();
  const daysViewInit = jest.fn();
  const milesViewInit = jest.fn();
  const detailsView = {
    init: detailsInit,
    render: detailsRender
  };
  const viewMock = mock => () => ( {
    init: mock
  } );
  const costViewMock = viewMock( costViewInit );
  costViewMock.CLASSES = averageCostView.CLASSES;

  const daysPerWeekViewMock = viewMock( daysViewInit );
  daysPerWeekViewMock.CLASSES = daysPerWeekView.CLASSES;

  const milesViewMock = viewMock( milesViewInit );
  milesViewMock.CLASSES = milesView.CLASSES;

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
    view = routeOptionFormView( document.querySelector( `.${ CLASSES.FORM }` ), {
      store,
      routeIndex: 0,
      detailsView,
      averageCostView: costViewMock,
      daysPerWeekView: daysPerWeekViewMock,
      milesView: milesViewMock
    } );
    view.init();
  } );

  afterEach( () => {
    dispatch.mockReset();
    view = null;
  } );

  it( 'initializes its children', () => {
    expect( costViewInit ).toHaveBeenCalled();
    expect( detailsInit ).toHaveBeenCalled();
    expect( daysViewInit ).toHaveBeenCalled();
    expect( milesViewInit ).toHaveBeenCalled();
  } );


  it( 'dispatches an action to update `transportation` with checkbox selection', () => {
    const radioEl = document.querySelectorAll( 'input[name="transpo"]' )[0];

    simulateEvent( 'click', radioEl );

    const mock = store.dispatch.mock;

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual( updateTransportationAction( { routeIndex: 0, value: radioEl.value } ) );
  } );
} );
