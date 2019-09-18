import { simulateEvent } from '../../../../util/simulate-event';
import budgetFormView from '../../../../../cfgov/unprocessed/apps/youth-employment-success/js/budget-form-view';
import { configureStore } from '../../../../../cfgov/unprocessed/apps/youth-employment-success/js/store';

const HTML = `
<section class="block o-yes-budget">
  <h2>How much can you spend getting to work?</h1>
  <p>This section helps you budget</p>
  <form id="yes-budget-form" class="block__sub">
    <div class="content-l content-l__large-gutters block__sub">
      <div class="content-l_col content-l_col-1-3">
        <label for="money-earned" class="a-label">
          <b>How much money do you receive each month?</b>
        </label>
        <div>
          <p class="a-label_helper">
            Some sources might be:
          </p>
          <ul class="a-label_helper">
            <li>Source 1</li>
            <li>Source 2</li>
            <li>Source 3</li>
          </ul>
        </div>
      </div>
      <div class="content-l_col content-l_col-2-3">
        <input type="text" name="money-earned" class="a-text-input o-yes-budget-earned">
      </div>
    </div>

    <div class="content-l content-l__large-gutters block__sub">
      <div class="content-l_col content-l_col-1-3">
        <label for="money-spent" class="a-label">
          <b>Now, subtract your monthy expenses:</b>
        </label>
        <div>
          <p class="a-label_helper">
            Don't include transportation costs. Examples of expenses:
          </p>
          <ul class="a-label_helper">
            <li>Source 1</li>
            <li>Source 2</li>
            <li>Source 3</li>
          </ul>
        </div>
      </div>
      
      <div class="content-l_col content-l_col-2-3">
        <span><b>(-)</b></span>
        <input type="text" name="money-spent" class="a-text-input o-yes-budget-spent">
      </div>
    </div>
  </form>
  <div class="content-l block__sub">
    <div class="content-l_col content-l_col-2-3">
      <div class="content_line-bold"></div>
      <div class="content-l">
        <div class="content-l_col content-l_col-3-4">
          <b>Total left at the end of the month:</b>
        </div>
        <div class="content-l_col content-l_col-1-4">
          <div class="content-l">
            <div class="content-l_col content-l_col-1-3">$</div>
            <div class="content-l_col content-l_col-2-3 o-yes-budget-remaining"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="content-l">
    <p class="content-l_col-1">Estimating your budget etc...</p>
  </div>
</section>
`;

describe( 'BudgetFormView', () => {
  const CLASSES = budgetFormView.CLASSES;
  let view;
  let store;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    store = configureStore();
    view = budgetFormView( document.querySelector( `.${ CLASSES.FORM }` ), { store } );
    view.init();
  } );

  afterEach( () => {
    view.destroy();
    view = null;
  } );

  it( 'updates the total when either/both money spent or earned values are present', () => {
    const moneySpentEl = document.querySelector( `.${ CLASSES.SPENT_INPUT }` );
    const moneyEarnedEl = document.querySelector( `.${ CLASSES.EARNED_INPUT }` );
    const totalEl = document.querySelector( `.${ CLASSES.REMAINING }` );

    moneyEarnedEl.value = '100';
    simulateEvent( 'input', moneyEarnedEl );

    expect( totalEl.textContent ).toEqual( '100' );

    moneySpentEl.value = '100';
    simulateEvent( 'input', moneySpentEl );

    expect( totalEl.textContent ).toEqual( '0' );
  } );

  it( 'defaults the `total` value to zero when no input has been received', () => {
    const totalEl = document.querySelector( `.${ CLASSES.REMAINING }` );
    expect( totalEl.textContent ).toEqual( '0' );
  } );

  it( 'unbinds events on view cleanup', () => {
    const moneySpentEl = document.querySelector( `.${ CLASSES.SPENT_INPUT }` );
    const totalEl = document.querySelector( `.${ CLASSES.REMAINING }` );

    moneySpentEl.value = '100';
    simulateEvent( 'input', moneySpentEl );

    view.destroy();

    moneySpentEl.value = '5';
    simulateEvent( 'input', moneySpentEl );

    expect( totalEl.textContent ).toEqual( '-100' );
  } );
} );
