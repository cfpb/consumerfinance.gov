import { observer } from 'mobx-react';
import { Link, useRouteMatch } from "react-router-dom";
import { useStore } from '../../../stores';
import { useEffect, useState, useCallback } from 'react';
import Button from '../../../components/button';

function StartingBalance() {
  const store = useStore();
  const { uiStore, eventStore } = store;

  // Local state to track user input in the form:
  const [startingBalance, setStartingBalance] = useState(0);

  // Local state talking to the global MobX cash flow event store
  // Add any variables from outside this function that you refer to, to the array on line 27.
  // See: https://reactjs.org/docs/hooks-reference.html#usecallback
  const addStartingBalance = useCallback((event) => {
    event.preventDefault();

    console.log('Starting balance is %s', startingBalance);

    eventStore.addEvent({
      name: 'Starting balance',
      date: new Date(),
      total: startingBalance,
      category: 'Starting Balance',
    });
  }, [startingBalance, eventStore]);

  // Outside of the render step, tell our UI store what the current page title is:
  useEffect(() => {
    uiStore.setPageTitle('Starting Balance');
    uiStore.setSubtitle('How much money are you starting with?');
  });

  return (
    <div className="step starting-balance">
      <img
        src="/static/apps/mmt-my-money-calendar/img/1.png"
        alt=""
        height="42"
        className="u-hide-on-print"
      />
      <img
        src="/static/apps/mmt-my-money-calendar/img/thinking.png"
        alt=""
        height="100"
        className="u-hide-on-print"
      />
      <h3>Let's figure out your Starting Balance</h3>
      <p>Where do you have money?</p>

      <form className="wizard-form" onSubmit={addStartingBalance}>
        <div className="wizard-form__field">
          <label htmlFor="starting-balance">Enter balance</label>
          <input id="starting-balance" value={startingBalance} onChange={(event) => setStartingBalance(event.target.value)} />
        </div>

        <Button type="submit">
          Add Starting Balance
        </Button>
      </form>

      <ul>
        <li>Checking account</li>
        <li>Savings account</li>
        <li>Cash</li>
        <li>Prepaid Cards</li>
        <li>Other</li>
        <li>None</li>
      </ul>
    </div>
  );
}

export default observer(StartingBalance);
