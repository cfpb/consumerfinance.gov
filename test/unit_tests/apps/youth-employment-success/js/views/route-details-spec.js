import routeDetailsView from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/route-details';
import { toArray, toPrecision } from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';
import { PLAN_TYPES } from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/data/todo-items';
import transportationMap from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/data/transportation-map';

const HTML = `
  <div class="yes-route-details">
    <p>
      Totals for <span class="js-transportation-type"></span>
    </p>  
    <div>
      <p class="content-l content-l_col-3-4">
        <b>Money left in your monthly budget</b>
      </p>
      <p class="content-l content-l_col-1-4">
        $<b class="content-l_col-2-3 js-budget"></b>
      </p>
      <div>
        Average monthly cost of <span class="js-transportation-type"></span>
        <span>
          Based on <span class="js-days-per-week"></span> days a week you will make this trip
        </span>
      </div>
      $<b class="content-l_col-2-3 js-total-cost"></b>
    </div>
    <div>   
      <b>Total left in your budget after <span class="js-transportation-type"></span></b>
      $<b class="content-l_col-2-3 js-budget-left"></b>
      <div class="js-route-incomplete"><p class="m-notification"></p></div>
      <div class="js-route-oob"><p class="m-notification"></p></div>
      <div class="js-route-complete"><p class="m-notification"></p></div>
    </div>
    <div>
      <p class="content-l content-l_col-1-3"><b>Total time to get to work</b></p>
      <p class="content-l content-l_col-2-3" style="text-align: right;">
        <b class="content-l_col-1-2">
          <span class="js-time-hours"></span> hours
        </b>
        <b class="content-l_col-1-2">
          <span class="js-time-minutes"></span> minutes
        </b>
      </p>
    </div>
    <div class="js-todo-list u-hidden">
      <span class="h4">MY TO-DO LIST</span> 
      <ul class="js-todo-items"></ul>
    </div>
  </div>
`;

describe( 'routeDetailsView', () => {
  const nextState = {
    budget: {
      earned: '100',
      spent: '25'
    },
    route: {
      transportation: 'Drive',
      daysPerWeek: '3',
      miles: '20',
      averageCost: '10',
      isMonthlyCost: null,
      transitTimeHours: '1',
      transitTimeMinutes: '5',
      actionPlanItems: [ PLAN_TYPES.TIME ]
    }
  };
  const CLASSES = routeDetailsView.CLASSES;
  let view;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    view = routeDetailsView(
      document.querySelector( `.${ CLASSES.CONTAINER }` )
    );
  } );

  afterEach( () => {
    view = null;
  } );

  describe( 'on state update', () => {
    it( 'updates its transportation type', () => {
      view.render( nextState );

      const transportationEls = toArray(
        document.querySelectorAll( `.${ CLASSES.TRANSPORTATION_TYPE }` )
      );

      const expected = transportationMap[nextState.route.transportation];

      transportationEls.forEach( el => expect( el.textContent ).toBe( expected )
      );
    } );

    it( 'updates its budget value', () => {
      view.render( nextState );

      const budgetEl = document.querySelector( `.${ CLASSES.BUDGET }` );
      const expectedBudget = toPrecision( String( nextState.budget.earned - nextState.budget.spent ), 2 );

      expect( budgetEl.textContent ).toBe( expectedBudget );
    } );

    it( 'updates its days per week value', () => {
      view.render( nextState );

      const daysPerWeekEl = document.querySelector( `.${ CLASSES.DAYS_PER_WEEK }` );

      expect( daysPerWeekEl.textContent ).toBe( nextState.route.daysPerWeek );
    } );

    describe( 'total costs', () => {
      it( 'correctly calculates driving cost', () => {
        view.render( nextState );

        const totalCostEl = document.querySelector( `.${ CLASSES.TOTAL_COST }` );

        expect( totalCostEl.textContent ).toBe( '432.00' );
      } );

      it( 'correctly calculates monthly cost', () => {
        const state = {
          budget: { ...nextState.budget },
          route: {
            ...nextState.route,
            transportation: 'Walk',
            isMonthlyCost: true,
            averageCost: '100'
          }
        };

        view.render( state );

        const totalCostEl = document.querySelector( `.${ CLASSES.TOTAL_COST }` );

        expect( totalCostEl.textContent ).toBe( '100.00' );
      } );

      it( 'correctly calculates monthly cost based on daily cost', () => {
        const state = {
          budget: { ...nextState.budget },
          route: {
            ...nextState.route,
            transportation: 'Walk',
            isMonthlyCost: false
          }
        };

        view.render( state );

        const totalCostEl = document.querySelector( `.${ CLASSES.TOTAL_COST }` );

        expect( totalCostEl.textContent ).toBe( '120.00' );
      } );

      it( 'does not update the total cost if daysPerWeek is not supplied', () => {
        const state = {
          budget: { ...nextState.budget },
          route: {
            ...nextState.route,
            transportation: 'Walk',
            isMonthlyCost: false,
            daysPerWeek: 0
          }
        };

        view.render( state );

        const totalCostEl = document.querySelector( `.${ CLASSES.TOTAL_COST }` );

        expect( totalCostEl.textContent ).toBe( '0.00' );
      } );

      it( 'updates total cost properly when daysPerWeek is supplied', () => {
        const state = {
          budget: { ...nextState.budget },
          route: {
            ...nextState.route,
            transportation: 'Walk',
            isMonthlyCost: false,
            daysPerWeek: 2,
            averageCost: '100'
          }
        };

        view.render( state );

        const totalCostEl = document.querySelector( `.${ CLASSES.TOTAL_COST }` );

        expect( totalCostEl.textContent ).toBe( '800.00' );
      } );
    } );

    it( 'updates its budget remaining', () => {
      view.render( nextState );

      const budgetLeftEl = document.querySelector( `.${ CLASSES.BUDGET_REMAINING }` );

      expect( budgetLeftEl.textContent ).toBe( `${ String.fromCharCode( 8722 ) }357.00` );
    } );

    it( 'updates the time in hours', () => {
      view.render( nextState );

      const hoursEl = document.querySelector( `.${ CLASSES.TIME_HOURS }` );

      expect( hoursEl.textContent ).toBe( '1' );
    } );

    it( 'updates the time in minutes', () => {
      view.render( nextState );

      const minutesEl = document.querySelector( `.${ CLASSES.TIME_MINUTES }` );

      expect( minutesEl.textContent ).toBe( '5' );
    } );

    it( 'shows the todo list when there are todo list items', () => {
      const todosEl = document.querySelector( `.${ CLASSES.TODO_LIST }` );

      expect( todosEl.classList.contains( 'u-hidden' ) ).toBeTruthy();

      view.render( nextState );

      expect( todosEl.classList.contains( 'u-hidden' ) ).toBeFalsy();
    } );

    it( 'updates the to-do list', () => {
      view.render( nextState );

      const todosEl = document.querySelector( `.${ CLASSES.TODO_LIST }` );
      const todoItemsEl = document.querySelector( `.${ CLASSES.TODO_ITEMS }` );

      expect( todoItemsEl.querySelectorAll( 'li' ).length ).toBe( 1 );

      view.render( {
        ...nextState,
        route: {
          ...nextState.route,
          actionPlanItems: []
        }
      } );

      expect( todosEl.classList.contains( 'u-hidden' ) ).toBeTruthy();
      expect( todoItemsEl.querySelectorAll( 'li' ).length ).toBe( 0 );
    } );

    it.only( 'does not hide the to-do list when an item is removed and there are remaining items', () => {
      const state = {
        budget: { ...nextState.budget },
        route: {
          ...nextState.route,
          actionPlanItems: nextState.route.actionPlanItems.concat( [ PLAN_TYPES.MILES ] )
        }
      };

      view.render( state );

      const todosEl = document.querySelector( `.${ CLASSES.TODO_LIST }` );
      const todoItemsEl = document.querySelector( `.${ CLASSES.TODO_ITEMS }` );

      expect( todoItemsEl.querySelectorAll( 'li' ).length ).toBe( 2 );

      view.render( {
        budget: { ...state.budget },
        route: {
          ...state.route,
          actionPlanItems: [ PLAN_TYPES.MILES ]
        }
      } );

      expect( todosEl.classList.contains( 'u-hidden' ) ).toBeFalsy();
    } );

    it( 'shows the out of budget alert when the route is out of budget', () => {
      const state = {
        budget: { earned: '1', spent: '100' },
        route: {
          ...nextState.route,
          transportation: 'Drive'
        }
      };

      view.render( state );

      const oobAlertEl = document.querySelector( `.${ CLASSES.OOB_ALERT }` );
      const notification = oobAlertEl.querySelector( '.m-notification' );
      expect( notification.classList.contains( 'm-notification__visible' ) ).toBeTruthy();
    } );

    it( 'displays incomplete alert message until all required fields are filled in', () => {
      view.render( nextState );

      let incAlertEl = document.querySelector( `.${ CLASSES.INCOMPLETE_ALERT }` );
      let notification = incAlertEl.querySelector( '.m-notification' );
      expect( notification.classList.contains( 'm-notification__visible' ) ).toBeFalsy();

      view.render( {
        ...nextState,
        route: {
          ...nextState.route,
          miles: 0
        }
      } );

      incAlertEl = document.querySelector( `.${ CLASSES.INCOMPLETE_ALERT }` );
      notification = incAlertEl.querySelector( '.m-notification' );
      expect( notification.classList.contains( 'm-notification__visible' ) ).toBeTruthy();
    } );

    it( 'displays a complete alert message when the data is valid and the option is in budget', () => {
      view.render( nextState );

      let completeAlert = document.querySelector( `.${ CLASSES.COMPLETE_ALERT }` );
      let notification = completeAlert.querySelector( '.m-notification' );

      expect( notification.classList.contains( 'm-notification__visible' ) ).toBeFalsy();

      const state = {
        budget: { earned: '10000', spent: '10' },
        route: {
          ...nextState.route,
          transportation: 'Drive'
        }
      };

      view.render( state );

      completeAlert = document.querySelector( `.${ CLASSES.COMPLETE_ALERT }` );
      notification = completeAlert.querySelector( '.m-notification' );

      expect( notification.classList.contains( 'm-notification__visible' ) ).toBeTruthy();
    } );
  } );
} );
