import reviewDetailsView from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/review/details';
import mockStore from '../../../../../mocks/store';
import { toArray } from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';
import { PLAN_TYPES } from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/data-types/todo-items';

let state;

const CLASSES = reviewDetailsView.CLASSES;

const HTML = `
<div class="${ CLASSES.CONTAINER }">
  <h2>Your plan to get to work</h2>
  <div class="block block__sub">
    <p class="h3 ${ CLASSES.CHOICE_HEADING }">Your first choice is <span class="js-transportation-option"></span></p>
    <div class="yes-route-details">
      <div class="js-route-notification block block__sub-micro block__flush-top u-hidden"></div>
      <div class="js-todo-list">
        <ul class="js-todo-items">
          <li>default todo</li>
        </ul>
      </div>
    </div>
    <div class="content_line"></div>
  </div>
  <div class="block block__sub">
    <div class="${ CLASSES.CHOICE_HEADING }">
      <p class="h3">Another option you compared: <span class="js-transportation-option"></span></p>
      <p>Depending on whether this fits in your budget and schedule, this could be a backup plan if you’re in a bind and your first choice doesn’t work out.</p>
    </div>
    <div class="yes-route-details">
      <div class="js-route-notification block block__sub-micro block__flush-top u-hidden"></div>
      <div class="js-todo-list">        
        <ul class="js-todo-items">
          <li>default todo</li>
        </ul>
      </div>
    </div>
    <div class="content_line"></div>
  </div>
</div>
`;

describe( 'reviewDetailsView', () => {
  const initMock = jest.fn();
  const renderMock = jest.fn();
  const routeDetailsView = () => ( {
    init: initMock,
    render: renderMock
  } );
  let el;
  let store;
  let view;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    el = document.querySelector( `.${ reviewDetailsView.CLASSES.CONTAINER }` );
    store = mockStore();
    store.mockState( {
      routes: { routes: []}
    } );
    view = reviewDetailsView( el, { store, routeDetailsView } );
    view.init();
  } );

  afterEach( () => {
    store.mockReset();
    initMock.mockReset();
    view = null;
  } );

  it( 'subscribes to the store on init', () => {
    expect( store.subscribe.mock.calls.length ).toBe( 1 );
  } );

  it( 'initializes its two routeDetails subviews on init', () => {
    expect( initMock.mock.calls.length ).toBe( 2 );
  } );

  describe.only( 'on state update', () => {
    const budget = { earned: 1, spent: 1 };
    const actionPlanRoute = { transportation: 'Walk', actionPlanItems: [ PLAN_TYPES.MILES ]};

    state = {
      budget,
      routes: {
        routes: [
          actionPlanRoute,
          { transportation: 'Drive' }
        ]
      }
    };

    it( 'renders the details views', () => {
      store.subscriber()( {}, state );

      expect( renderMock.mock.calls.length ).toBe( 2 );
    } );

    it( 'hides the `Possible Option` headings when the user selects the `wait` choice', () => {
      state = {
        budget,
        routes: { routes: []},
        routeChoice: 'wait'
      };

      store.subscriber()( {}, state );

      const choiceHeadings = toArray( el.querySelectorAll( `.${ CLASSES.CHOICE_HEADING }` ) );

      choiceHeadings.forEach( ch => {
        expect( ch.classList.contains( 'u-hidden' ) ).toBeTruthy();
      } );
    } );
  } );
} );
